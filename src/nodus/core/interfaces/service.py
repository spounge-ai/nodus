import grpc
import logging

from nodus.protos import svc, svc_grpc
from nodus.protos.nodes import execution
from nodus.protos.mcp import connection as mcp_connection
from nodus.core.application.node_executor import NodeExecutor
from nodus.core.application.mcp_router import MCPRouter

logger = logging.getLogger(__name__)

class NodusService(svc_grpc.NodusServiceServicer):
    def __init__(self):
        self.node_executor = NodeExecutor()
        self.mcp_router = MCPRouter()
        logger.info("NodusService initialized.")

    async def ExecuteNode(
        self, request: execution.ExecuteNodeRequest, context: grpc.aio.ServicerContext
    ) -> execution.ExecuteNodeResponse:
        return await self.node_executor.execute(request, context)

    async def ExecuteNodeStream(
        self,
        request: execution.ExecuteNodeStreamRequest,
        context: grpc.aio.ServicerContext,
    ) -> execution.ExecuteNodeStreamResponse:
        logger.info(f"ExecuteNodeStream called for node_id: {request.node_id}")
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("ExecuteNodeStream is not yet implemented.")
        raise NotImplementedError("ExecuteNodeStream is not yet implemented.")

    async def RegisterMCPServer(
        self,
        request: mcp_connection.RegisterMCPServerRequest,
        context: grpc.aio.ServicerContext,
    ) -> mcp_connection.RegisterMCPServerResponse:
        return await self.mcp_router.register_mcp_server(request, context)

    async def ListMCPServers(
        self,
        request: mcp_connection.ListMCPServersRequest,
        context: grpc.aio.ServicerContext,
    ) -> mcp_connection.ListMCPServersResponse:
        return await self.mcp_router.list_mcp_servers(request, context)

    async def QueryMCPTools(
        self,
        request: mcp_connection.QueryMCPToolsRequest,
        context: grpc.aio.ServicerContext,
    ) -> mcp_connection.QueryMCPToolsResponse:
        return await self.mcp_router.query_mcp_tools(request, context)

    async def CheckHealth(
        self, request: svc.CheckHealthRequest, context: grpc.aio.ServicerContext
    ) -> svc.CheckHealthResponse:
        logger.info(f"Health check requested for service: '{request.service or 'all'}'")
        return svc.CheckHealthResponse(status=svc.CheckHealthResponse.ServingStatus.SERVING_STATUS_SERVING)
