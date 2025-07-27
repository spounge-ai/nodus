import grpc
import logging
from google.protobuf import any_pb2, struct_pb2
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, List
from langchain_core.tools import Tool
from langchain.agents import create_tool_calling_agent

from nodus.protos.nodes import execution as nodes_execution
from nodus.protos.common import types as common_types

from nodus.core.domain.executors.base_executor import BaseExecutor
from nodus.core.mcp.client import MCPClient
from nodus.core.domain.controllers.llm_manager import LLMManager
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

class AgentState(TypedDict):
    messages: Annotated[List[AIMessage | HumanMessage], lambda x, y: x + y]

class AutonomousExecutor(BaseExecutor):
    def __init__(self, mcp_client: MCPClient, llm_manager: LLMManager):
        self.mcp_client = mcp_client
        self.llm_manager = llm_manager

    async def execute(
        self, request: nodes_execution.ExecuteNodeRequest, context: grpc.aio.ServicerContext
    ) -> nodes_execution.ExecuteNodeResponse:
        logger.info(f"Executing autonomous node: {request.node_id}")

        llm_config = request.autonomous_config.llm_config
        llm = self.llm_manager.get_llm(llm_config)
        tools = self._get_tools(request.autonomous_config.tool_scope.allowed_tools)

        agent_runnable = create_tool_calling_agent(llm, tools, llm) # Using the dynamically selected LLM for agent creation

        workflow = StateGraph(AgentState)
        workflow.add_node("agent", agent_runnable)
        workflow.add_node("tools", self._tools_node)
        workflow.set_entry_point("agent")
        workflow.add_conditional_edges(
            "agent",
            self._should_continue,
            {"continue": "tools", "end": END}
        )
        workflow.add_edge('tools', 'agent')
        graph = workflow.compile()

        inputs = {"messages": [HumanMessage(content=request.autonomous_config.objective)]}
        result = await graph.ainvoke(inputs)

        result_struct = struct_pb2.Struct()
        result_struct.update({"final_message": result["messages"][-1].content})
        any_result = any_pb2.Any()
        any_result.Pack(result_struct)

        return nodes_execution.ExecuteNodeResponse(
            execution_id=request.execution_id,
            node_id=request.node_id,
            status=common_types.EXECUTION_STATUS_COMPLETED,
            result_data=any_result,
        )

    async def _agent_node(self, state):
        # This node will be replaced by the agent_runnable directly
        pass

    async def _tools_node(self, state):
        tool_calls = state["messages"][-1].tool_calls
        tool_outputs = []
        for tool_call in tool_calls:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_func = self.mcp_client.get_tool_by_name(tool_name)
            if tool_func:
                output = tool_func["__call__"](**tool_args) # Assuming __call__ is the function
                tool_outputs.append(AIMessage(content=str(output)))
            else:
                tool_outputs.append(AIMessage(content=f"Tool {tool_name} not found."))
        return {"messages": tool_outputs}

    def _should_continue(self, state):
        if len(state["messages"]) > 5:
            return "end"
        return "continue"

    def _get_tools(self, allowed_tools):
        tool_definitions = self.mcp_client.get_all_tools()
        return [self._create_pydantic_tool(t) for t in tool_definitions if t["name"] in allowed_tools]

    def _create_pydantic_tool(self, tool_info):
        def tool_function(**kwargs):
            logger.info(f"Executing tool: {tool_info['name']} with params: {kwargs}")
            return {"status": "success", "result": "mock tool output"}

        type_mapping = {
            "string": str,
            "number": float,
            "boolean": bool,
            "array": list,
            "object": dict,
        }

        annotations = {}
        for k, v in tool_info["input_schema"]["properties"].items():
            python_type = type_mapping.get(v["type"], str)
            annotations[k] = (python_type, Field(description=v.get("description", "")))

        DynamicToolModel = type(tool_info["name"], (BaseModel,), {
            "__doc__": tool_info["description"],
            "__annotations__": annotations,
        })

        return Tool(
            name=tool_info["name"],
            description=tool_info["description"],
            func=tool_function,
            args_schema=DynamicToolModel
        )
