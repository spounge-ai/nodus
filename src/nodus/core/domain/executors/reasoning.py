import grpc
import logging
from google.protobuf import any_pb2, struct_pb2
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from nodus.core.domain.controllers.llm_manager import LLMManager
from langchain_core.tools import Tool

from nodus.protos import nodes, common
from nodus.core.domain.executors.base_executor import BaseExecutor
from nodus.core.mcp.client import MCPClient

logger = logging.getLogger(__name__)

class ReasoningExecutor(BaseExecutor):
    def __init__(self, mcp_client: MCPClient, llm_manager: LLMManager):
        self.mcp_client = mcp_client
        self.llm_manager = llm_manager

    async def execute(
        self, request: nodes.execution.ExecuteNodeRequest, context: grpc.aio.ServicerContext
    ) -> nodes.execution.ExecuteNodeResponse:
        logger.info(f"Executing reasoning node: {request.node_id}")

        llm_config = request.reasoning_config.llm_config
        llm = self.llm_manager.get_llm(llm_config)
        tools = self._get_tools(request.reasoning_config.allowed_tools)
        llm_with_tools = llm.bind_tools(tools)

        # 2. Construct the prompt
        prompt = ChatPromptTemplate.from_messages([
            ("system", request.reasoning_config.system_prompt),
            ("user", "{input}")
        ])

        # 3. Create and invoke the chain
        chain = prompt | llm_with_tools
        result = await chain.ainvoke({"input": request.reasoning_config.user_prompt})

        # 4. Process and return the result
        result_struct = self._format_result(result)
        any_result = any_pb2.Any()
        any_result.Pack(result_struct)

        return nodes.execution.ExecuteNodeResponse(
            execution_id=request.execution_id,
            node_id=request.node_id,
            status=common.types.EXECUTION_STATUS_COMPLETED,
            result_data=any_result,
        )

    def _get_tools_from_mcp(self, allowed_tools):
        # Dynamically fetches and creates Pydantic models for tools from the MCP.
        tool_definitions = self.mcp_client.get_all_tools()
        return [self._create_pydantic_tool(t) for t in tool_definitions if t["name"] in allowed_tools]

    def _create_pydantic_tool(self, tool_info):
        # Creates a Pydantic model from the tool's schema.
        def tool_function(**kwargs):
            # This is a mock function. In a real scenario, this would
            # execute the tool via the MCP client.
            logger.info(f"Executing tool: {tool_info['name']} with params: {kwargs}")
            return {"status": "success", "result": "mock tool output"}

        type_mapping = {
            "string": str,
            "number": float,  # Use float for generic numbers, can be refined to int if needed
            "boolean": bool,
            "array": list,
            "object": dict,
        }

        annotations = {}
        for k, v in tool_info["input_schema"]["properties"].items():
            python_type = type_mapping.get(v["type"], str)  # Default to str if type not found
            annotations[k] = (python_type, Field(description=v.get("description", "")))

        # Create a dynamic Pydantic model
        DynamicToolModel = type(tool_info["name"], (BaseModel,), {
            "__doc__": tool_info["description"],
            "__annotations__": annotations,
        })

        # Attach the tool_function to an instance of the dynamic model
        # This is a simplified approach. In a real scenario, you might use
        # a custom Tool class that wraps the Pydantic model and the function.
        # For now, we'll just return a callable that mimics the tool interface.
        def callable_tool(**kwargs):
            return tool_function(**kwargs)

        return Tool(
            name=tool_info["name"],
            description=tool_info["description"],
            func=tool_function,
            args_schema=DynamicToolModel
        )

    def _format_result(self, result):
        # Formats the LangChain result into a protobuf Struct.
        output = {
            "content": result.content,
            "tool_calls": [
                {
                    "name": call["name"],
                    "args": call["args"],
                }
                for call in result.tool_calls
            ],
        }
        result_struct = struct_pb2.Struct()
        result_struct.update(output)
        return result_struct
