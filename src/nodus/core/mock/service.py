# src/nodus/core/mock/service.py
import grpc
import logging
import json
import asyncio
from concurrent import futures
from google.protobuf import duration_pb2
from google.protobuf import any_pb2
from google.protobuf import struct_pb2
from google.protobuf import timestamp_pb2
from datetime import datetime, timezone

from nodus.protos import svc, svc_grpc
from nodus.protos.nodes import execution_pb2 as execution
from nodus.protos.common import types_pb2 as common_types
from nodus.protos.mcp import connection_pb2 as mcp_connection
from nodus.protos.mcp import tool_pb2 as mcp_tool
from nodus.protos.mcp import server_pb2 as mcp_server
from nodus.core.mock.data import MOCK_NODE_DATA

logger = logging.getLogger(__name__)

class MockNodusService(svc_grpc.NodusServiceServicer):
    def __init__(self):
        self.mock_servers = {}
        self.mock_tools = []
        logger.info("MockNodusService initialized")

    def _create_execution_metadata(self, node_type, execution_time_seconds=2):
        metadata = execution.ExecutionMetadata()
        metadata.total_iterations = 1
        metadata.tool_invocations = 0 if node_type == "direct" else 1
        metadata.llm_processing_time.CopyFrom(duration_pb2.Duration(seconds=1))
        metadata.tool_execution_time.CopyFrom(duration_pb2.Duration(seconds=execution_time_seconds-1))
        metadata.serialization_time.CopyFrom(duration_pb2.Duration(nanos=100000000))
        metadata.confidence_score = 0.95
        metadata.termination_reason = "completed_successfully"
        
        step = execution.ExecutionStep()
        step.step_number = 1
        step.step_type = execution.StepType.STEP_TYPE_TOOL_INVOCATION
        step.description = f"Executed {node_type} node"
        step.step_duration.CopyFrom(duration_pb2.Duration(seconds=execution_time_seconds))
        step.step_status = common_types.ExecutionStatus.EXECUTION_STATUS_COMPLETED
        metadata.execution_steps.append(step)
        
        return metadata

    def _create_mock_result_data(self, node_type, node_id):
        result = {
            "node_id": node_id,
            "node_type": node_type,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "data": MOCK_NODE_DATA.get(node_type, {"default": "mock_result"})
        }
        
        struct_result = struct_pb2.Struct()
        struct_result.update(result)
        
        any_result = any_pb2.Any()
        any_result.Pack(struct_result)
        return any_result

    async def ExecuteNode(self, request: execution.ExecuteNodeRequest, context):
        logger.info(f"Executing node: {request.node_id} (type: {common_types.NodeType.Name(request.node_type)})")
        
        await asyncio.sleep(0.1)
        
        node_type_name = common_types.NodeType.Name(request.node_type).lower().replace("node_type_", "")
        
        if node_type_name not in MOCK_NODE_DATA:
            logger.error(f"Unknown node type: {node_type_name}")
            return execution.ExecuteNodeResponse(
                execution_id=request.execution_id,
                node_id=request.node_id,
                status=common_types.ExecutionStatus.EXECUTION_STATUS_FAILED,
                error=self._create_error("Unknown node type", node_type_name)
            )

        execution_time = 2 + hash(request.node_id) % 3
        
        response = execution.ExecuteNodeResponse()
        response.execution_id = request.execution_id
        response.node_id = request.node_id
        response.status = common_types.ExecutionStatus.EXECUTION_STATUS_COMPLETED
        response.result_data.CopyFrom(self._create_mock_result_data(node_type_name, request.node_id))
        response.metadata.CopyFrom(self._create_execution_metadata(node_type_name, execution_time))
        response.execution_time.CopyFrom(duration_pb2.Duration(seconds=execution_time))
        response.completed_at.CopyFrom(timestamp_pb2.Timestamp(seconds=int(datetime.now(timezone.utc).timestamp())))

        logger.info(f"Node {request.node_id} executed successfully in {execution_time}s")
        return response

    async def ExecuteNodeStream(self, request, context):
        logger.info(f"Streaming execution for node: {request.node_id}")
        
        node_type_name = common_types.NodeType.Name(request.node_type).lower().replace("node_type_", "")
        total_steps = 3
        
        for step in range(1, total_steps + 1):
            await asyncio.sleep(0.5)
            
            status = common_types.ExecutionStatus.EXECUTION_STATUS_RUNNING
            if step == total_steps:
                status = common_types.ExecutionStatus.EXECUTION_STATUS_COMPLETED
            
            response = execution.ExecuteNodeStreamResponse()
            response.execution_id = request.execution_id
            response.node_id = request.node_id
            response.status = status
            
            if step == total_steps:
                response.result_data.CopyFrom(self._create_mock_result_data(node_type_name, request.node_id))
                response.execution_time.CopyFrom(duration_pb2.Duration(seconds=step))
                response.completed_at.CopyFrom(timestamp_pb2.Timestamp(seconds=int(datetime.now(timezone.utc).timestamp())))
            
            yield response

    async def RegisterMCPServer(self, request: mcp_connection.RegisterMCPServerRequest, context):
        logger.info(f"Registering MCP server: {request.server_id} at {request.endpoint}")
        
        capabilities = mcp_server.MCPServerCapabilities()
        capabilities.protocol_version = "1.0"
        capabilities.supported_features.extend(["tools", "resources"])
        capabilities.max_concurrent_requests = 10
        capabilities.supports_streaming = True
        
        self.mock_servers[request.server_id] = {
            "endpoint": request.endpoint,
            "type": request.server_type,
            "status": mcp_server.MCPServerStatus.MCP_SERVER_STATUS_HEALTHY
        }
        
        mock_tools = [
            mcp_tool.MCPTool(
                tool_id=f"{request.server_id}_tool_1",
                server_id=request.server_id,
                name="mock_calculator",
                description="A mock calculator tool",
                category=mcp_tool.ToolCategory.TOOL_CATEGORY_COMPUTATION
            ),
            mcp_tool.MCPTool(
                tool_id=f"{request.server_id}_tool_2", 
                server_id=request.server_id,
                name="mock_data_fetcher",
                description="A mock data fetching tool",
                category=mcp_tool.ToolCategory.TOOL_CATEGORY_DATA_ACCESS
            )
        ]
        
        return mcp_connection.RegisterMCPServerResponse(
            success=True,
            server_id=request.server_id,
            capabilities=capabilities,
            available_tools=mock_tools
        )

    async def ListMCPServers(self, request: mcp_connection.ListMCPServersRequest, context):
        logger.info("Listing MCP servers")
        
        servers = []
        for server_id, server_data in self.mock_servers.items():
            if not request.server_ids or server_id in request.server_ids:
                server_info = mcp_server.MCPServerInfo()
                server_info.server_id = server_id
                server_info.name = f"Mock Server {server_id}"
                server_info.endpoint = server_data["endpoint"]
                server_info.server_type = server_data["type"]
                server_info.status = server_data["status"]
                server_info.registered_at.CopyFrom(timestamp_pb2.Timestamp(seconds=int(datetime.now(timezone.utc).timestamp())))
                servers.append(server_info)
        
        return mcp_connection.ListMCPServersResponse(
            servers=servers,
            total_servers=len(servers)
        )

    async def QueryMCPTools(self, request: mcp_connection.QueryMCPToolsRequest, context):
        logger.info("Querying MCP tools")
        
        tools = []
        for server_id in self.mock_servers.keys():
            if not request.server_ids or server_id in request.server_ids:
                tools.extend([
                    mcp_tool.MCPTool(
                        tool_id=f"{server_id}_calculator",
                        server_id=server_id,
                        name="calculator",
                        description="Performs mathematical calculations",
                        category=mcp_tool.ToolCategory.TOOL_CATEGORY_COMPUTATION
                    ),
                    mcp_tool.MCPTool(
                        tool_id=f"{server_id}_fetcher",
                        server_id=server_id,
                        name="data_fetcher", 
                        description="Fetches data from external sources",
                        category=mcp_tool.ToolCategory.TOOL_CATEGORY_DATA_ACCESS
                    )
                ])
        
        return mcp_connection.QueryMCPToolsResponse(
            tools=tools,
            total_matches=len(tools)
        )

    async def CheckHealth(self, request: svc.CheckHealthRequest, context):
        logger.info(f"Health check for service: {request.service}")
        return svc.CheckHealthResponse(
            status=svc.CheckHealthResponse.SERVING_STATUS_SERVING
        )

    def _create_error(self, message, details=""):
        from nodus.protos.common import errors_pb2 as common_errors
        error = common_errors.ExecutionError()
        error.error_type = common_errors.ErrorType.ERROR_TYPE_VALIDATION
        error.error_code = "MOCK_ERROR"
        error.error_message = message
        if details:
            error.stack_trace = f"Details: {details}"
        error.retryable = False
        return error