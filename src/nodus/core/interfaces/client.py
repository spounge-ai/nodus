# src/nodus/core/client.py
import asyncio
import grpc
import logging
import uuid
import json
from datetime import datetime, timezone
from google.protobuf import timestamp_pb2, duration_pb2, struct_pb2
from google.protobuf.json_format import MessageToDict

from nodus.protos import nodes, common, mcp, integrations
from nodus.protos.service import svc_grpc

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NodusTestClient:
    def __init__(self, server_address='localhost:50052'):
        self.server_address = server_address
        self.channel = None
        self.stub = None

    async def __aenter__(self):
        self.channel = grpc.aio.insecure_channel(self.server_address)
        self.stub = svc_grpc.NodusServiceStub(self.channel)
        logger.info(f"Connected to Nodus server at {self.server_address}")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.channel:
            await self.channel.close()

    def _create_execution_context(self, workflow_id="test-workflow"):
        return common.types.ExecutionContext(
            execution_id=str(uuid.uuid4()),
            workflow_id=workflow_id,
            user_id="test-user",
            created_at=timestamp_pb2.Timestamp(seconds=int(datetime.now(timezone.utc).timestamp()))
        )

    async def test_direct_node(self):
        logger.info("=== Testing Direct Node ===")
        
        context = self._create_execution_context()
        
        tool_params = struct_pb2.Struct()
        tool_params.update({"operand1": 10, "operand2": 5, "operation": "add"})
        
        direct_config = nodes.direct.DirectNodeConfig(
            mcp_server_id="calculator-server",
            tool_name="calculator",
            tool_parameters=tool_params,
            tool_timeout=duration_pb2.Duration(seconds=5),
            validate_parameters=True
        )

        request = nodes.execution.ExecuteNodeRequest(
            execution_id=context.execution_id,
            node_id="direct-calc-001",
            node_type=common.types.NodeType.NODE_TYPE_DIRECT,
            timeout=duration_pb2.Duration(seconds=10),
            max_retries=2,
            direct_config=direct_config,
            execution_context=context,
            requested_at=timestamp_pb2.Timestamp(seconds=int(datetime.now(timezone.utc).timestamp()))
        )

        response = await self.stub.ExecuteNode(request)
        self._print_execution_result(response)
        return response

    async def test_reasoning_node(self):
        logger.info("=== Testing Reasoning Node ===")
        
        context = self._create_execution_context()
        
        # Test with OpenAI LLM
        llm_config_openai = integrations.llm.LLMConfiguration(
            provider=integrations.llm.LLMProvider.LLM_PROVIDER_OPENAI,
            model_name="gpt-4-turbo",
            credential_id="openai-api-key"
        )
        llm_params_openai = integrations.llm.LLMParameters(temperature=0.7)
        reasoning_config_openai = nodes.reasoning.ReasoningNodeConfig(
            llm_config=llm_config_openai,
            model_parameters=llm_params_openai,
            system_prompt="You are a helpful AI assistant that thinks step by step.",
            user_prompt="Analyze the pros and cons of remote work.",
            reasoning_timeout=duration_pb2.Duration(seconds=30)
        )
        request_openai = nodes.execution.ExecuteNodeRequest(
            execution_id=context.execution_id + "-openai",
            node_id="reasoning-openai-001",
            node_type=common.types.NodeType.NODE_TYPE_REASONING,
            timeout=duration_pb2.Duration(seconds=45),
            max_retries=1,
            reasoning_config=reasoning_config_openai,
            execution_context=context,
            requested_at=timestamp_pb2.Timestamp(seconds=int(datetime.now(timezone.utc).timestamp()))
        )
        response_openai = await self.stub.ExecuteNode(request_openai)
        self._print_execution_result(response_openai)

        # Test with Google Gemini LLM
        llm_config_gemini = integrations.llm.LLMConfiguration(
            provider=integrations.llm.LLMProvider.LLM_PROVIDER_GOOGLE,
            model_name="gemini-pro",
            credential_id="gemini-api-key"
        )
        reasoning_config_gemini = nodes.reasoning.ReasoningNodeConfig(
            llm_config=llm_config_gemini,
            model_parameters=integrations.llm.LLMParameters(temperature=0.5),
            system_prompt="You are a concise AI assistant.",
            user_prompt="Summarize the benefits of renewable energy.",
            reasoning_timeout=duration_pb2.Duration(seconds=30)
        )
        request_gemini = nodes.execution.ExecuteNodeRequest(
            execution_id=context.execution_id + "-gemini",
            node_id="reasoning-gemini-001",
            node_type=common.types.NodeType.NODE_TYPE_REASONING,
            timeout=duration_pb2.Duration(seconds=45),
            max_retries=1,
            reasoning_config=reasoning_config_gemini,
            execution_context=context,
            requested_at=timestamp_pb2.Timestamp(seconds=int(datetime.now(timezone.utc).timestamp()))
        )
        response_gemini = await self.stub.ExecuteNode(request_gemini)
        self._print_execution_result(response_gemini)
        return response_gemini # Return the last response for consistency with original method signature

    async def test_autonomous_node(self):
        logger.info("=== Testing Autonomous Node ===")
        
        context = self._create_execution_context()
        
        # Test with OpenAI LLM
        llm_config_openai = integrations.llm.LLMConfiguration(
            provider=integrations.llm.LLMProvider.LLM_PROVIDER_ANTHROPIC,
            model_name="claude-3",
            credential_id="anthropic-key"
        )
        autonomous_config_openai = nodes.autonomous.AutonomousNodeConfig(
            llm_config=llm_config_openai,
            agent_type=nodes.autonomous.AgentType.AGENT_TYPE_REACT,
            objective="Research and summarize the latest developments in AI safety",
            system_context="You are an AI research assistant with access to various tools.",
            max_iterations=5,
            max_execution_time=duration_pb2.Duration(seconds=120),
            confidence_threshold=0.8,
            enable_streaming=False
        )
        request_openai = nodes.execution.ExecuteNodeRequest(
            execution_id=context.execution_id + "-openai",
            node_id="autonomous-openai-001",
            node_type=common.types.NodeType.NODE_TYPE_AUTONOMOUS,
            timeout=duration_pb2.Duration(seconds=150),
            max_retries=1,
            autonomous_config=autonomous_config_openai,
            execution_context=context,
            requested_at=timestamp_pb2.Timestamp(seconds=int(datetime.now(timezone.utc).timestamp()))
        )
        response_openai = await self.stub.ExecuteNode(request_openai)
        self._print_execution_result(response_openai)

        # Test with Google Gemini LLM
        llm_config_gemini = integrations.llm.LLMConfiguration(
            provider=integrations.llm.LLMProvider.LLM_PROVIDER_GOOGLE,
            model_name="gemini-pro",
            credential_id="gemini-api-key"
        )
        autonomous_config_gemini = nodes.autonomous.AutonomousNodeConfig(
            llm_config=llm_config_gemini,
            agent_type=nodes.autonomous.AgentType.AGENT_TYPE_PLANNING,
            objective="Develop a marketing strategy for a new eco-friendly product.",
            system_context="You are a marketing expert AI with access to market research tools.",
            max_iterations=7,
            max_execution_time=duration_pb2.Duration(seconds=180),
            confidence_threshold=0.9,
            enable_streaming=False
        )
        request_gemini = nodes.execution.ExecuteNodeRequest(
            execution_id=context.execution_id + "-gemini",
            node_id="autonomous-gemini-001",
            node_type=common.types.NodeType.NODE_TYPE_AUTONOMOUS,
            timeout=duration_pb2.Duration(seconds=200),
            max_retries=1,
            autonomous_config=autonomous_config_gemini,
            execution_context=context,
            requested_at=timestamp_pb2.Timestamp(seconds=int(datetime.now(timezone.utc).timestamp()))
        )
        response_gemini = await self.stub.ExecuteNode(request_gemini)
        self._print_execution_result(response_gemini)
        return response_gemini # Return the last response for consistency with original method signature

    async def test_webhook_node(self):
        logger.info("=== Testing Webhook Node ===")
        
        context = self._create_execution_context()
        
        webhook_config = nodes.webhook.WebhookNodeConfig(
            listen_id="webhook-listener-001",
            timeout=duration_pb2.Duration(seconds=30),
            verification_config_name="default-webhook-verification"
        )

        request = nodes.execution.ExecuteNodeRequest(
            execution_id=context.execution_id,
            node_id="webhook-001",
            node_type=common.types.NodeType.NODE_TYPE_WEBHOOK,
            timeout=duration_pb2.Duration(seconds=60),
            max_retries=0,
            webhook_config=webhook_config,
            execution_context=context,
            requested_at=timestamp_pb2.Timestamp(seconds=int(datetime.now(timezone.utc).timestamp()))
        )

        response = await self.stub.ExecuteNode(request)
        self._print_execution_result(response)
        return response

    async def test_streaming_execution(self):
        logger.info("=== Testing Streaming Execution ===")
        
        context = self._create_execution_context()
        
        autonomous_config = nodes.autonomous.AutonomousNodeConfig(
            agent_type=nodes.autonomous.AgentType.AGENT_TYPE_PLANNING,
            objective="Plan a multi-step data analysis workflow",
            max_iterations=3,
            enable_streaming=True,
            stream_interval_ms=1000
        )

        request = nodes.execution.ExecuteNodeStreamRequest(
            execution_id=context.execution_id,
            node_id="streaming-autonomous-001",
            node_type=common.types.NodeType.NODE_TYPE_AUTONOMOUS,
            timeout=duration_pb2.Duration(seconds=30),
            autonomous_config=autonomous_config,
            execution_context=context,
            requested_at=timestamp_pb2.Timestamp(seconds=int(datetime.now(timezone.utc).timestamp()))
        )

        async for response in self.stub.ExecuteNodeStream(request):
            logger.info(f"Stream update - Status: {common.types.ExecutionStatus.Name(response.status)}")
            if response.status == common.types.ExecutionStatus.EXECUTION_STATUS_COMPLETED:
                self._print_execution_result(response)
                break

    async def test_mcp_operations(self):
        logger.info("=== Testing MCP Operations ===")
        
        register_request = mcp.connection.RegisterMCPServerRequest(
            server_id="test-mcp-server",
            endpoint="http://localhost:8080/mcp",
            server_type=1,
            metadata={"version": "1.0", "provider": "test"}
        )
        
        register_response = await self.stub.RegisterMCPServer(register_request)
        logger.info(f"MCP Server registered: {register_response.success}")
        
        list_request = mcp.connection.ListMCPServersRequest(include_tools=True)
        list_response = await self.stub.ListMCPServers(list_request)
        logger.info(f"Found {list_response.total_servers} MCP servers")
        
        tools_request = mcp.connection.QueryMCPToolsRequest(
            server_ids=["test-mcp-server"],
            limit=10
        )
        tools_response = await self.stub.QueryMCPTools(tools_request)
        logger.info(f"Found {tools_response.total_matches} tools")

    def _print_execution_result(self, response):
        logger.info("Execution Results:")
        logger.info(f"  Node ID: {response.node_id}")
        logger.info(f"  Status: {common.types.ExecutionStatus.Name(response.status)}")
        logger.info(f"  Execution Time: {response.execution_time.seconds}s")
        
        if response.metadata:
            logger.info(f"  Iterations: {response.metadata.total_iterations}")
            logger.info(f"  Tool Calls: {response.metadata.tool_invocations}")
            logger.info(f"  Confidence: {response.metadata.confidence_score}")
        
        if response.result_data:
            try:
                result_dict = MessageToDict(response.result_data)
                logger.info(f"  Result: {json.dumps(result_dict, indent=2)}")
            except Exception as e:
                logger.info(f"  Result: <unparseable: {e}>")
        
        if response.error and response.error.error_message:
            logger.error(f"  Error: {response.error.error_message}")

async def main():
    async with NodusTestClient() as client:
        try:
            await client.test_direct_node()
            await asyncio.sleep(1)
            
            await client.test_reasoning_node()
            await asyncio.sleep(1)
            
            await client.test_autonomous_node()
            await asyncio.sleep(1)
            
            await client.test_webhook_node()
            await asyncio.sleep(1)
            
            await client.test_streaming_execution()
            await asyncio.sleep(1)
            
            await client.test_mcp_operations()
            
        except grpc.aio.AioRpcError as e:
            logger.error(f"gRPC Error: {e.code().name} - {e.details()}")
        except Exception as e:
            logger.error(f"Unexpected error: {e}")

if __name__ == '__main__':
    asyncio.run(main())