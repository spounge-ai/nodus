import grpc
import logging

from nodus.protos import nodes, mcp
from nodus.protos.service import svc, svc_grpc
from nodus.core.application.node_executor import NodeExecutor
from nodus.core.application.mcp_router import MCPRouter

logger = logging.getLogger(__name__)

class NodusService(svc_grpc.NodusServiceServicer):
    def __init__(self):
        self.node_executor = NodeExecutor()
        self.mcp_router = MCPRouter()
        logger.info("NodusService initialized.")

    async def ExecuteNode(
        self, request: nodes.execution.ExecuteNodeRequest, context: grpc.aio.ServicerContext
    ) -> nodes.execution.ExecuteNodeResponse:
        return await self.node_executor.execute(request, context)

    async def ExecuteNodeStream(
        self,
        request: nodes.execution.ExecuteNodeStreamRequest,
        context: grpc.aio.ServicerContext,
    ) -> nodes.execution.ExecuteNodeStreamResponse:
        logger.info(f"ExecuteNodeStream called for node_id: {request.node_id}")
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("ExecuteNodeStream is not yet implemented.")
        raise NotImplementedError("ExecuteNodeStream is not yet implemented.")

    async def RegisterMCPServer(
        self,
        request: mcp.connection.RegisterMCPServerRequest,
        context: grpc.aio.ServicerContext,
    ) -> mcp.connection.RegisterMCPServerResponse:
        return await self.mcp_router.register_mcp_server(request, context)

    async def ListMCPServers(
        self,
        request: mcp.connection.ListMCPServersRequest,
        context: grpc.aio.ServicerContext,
    ) -> mcp.connection.ListMCPServersResponse:
        return await self.mcp_router.list_mcp_servers(request, context)

    async def QueryMCPTools(
        self,
        request: mcp.connection.QueryMCPToolsRequest,
        context: grpc.aio.ServicerContext,
    ) -> mcp.connection.QueryMCPToolsResponse:
        return await self.mcp_router.query_mcp_tools(request, context)

    async def CheckHealth(
        self, request: svc.CheckHealthRequest, context: grpc.aio.ServicerContext
    ) -> svc.CheckHealthResponse:
        logger.info(f"Health check requested for service: '{request.service or 'all'}'")
        return svc.CheckHealthResponse(status=svc.CheckHealthResponse.ServingStatus.SERVING_STATUS_SERVING)
