# src/nodus/core/application/mcp_router.py
import grpc
from nodus.protos.mcp import connection as mcp_connection

class MCPRouter:
    async def register_mcp_server(
        self, request: mcp_connection.RegisterMCPServerRequest, context: grpc.aio.ServicerContext
    ) -> mcp_connection.RegisterMCPServerResponse:
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("MCPRouter.register_mcp_server is not yet implemented.")
        raise NotImplementedError("MCPRouter.register_mcp_server is not yet implemented.")

    async def list_mcp_servers(
        self, request: mcp_connection.ListMCPServersRequest, context: grpc.aio.ServicerContext
    ) -> mcp_connection.ListMCPServersResponse:
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("MCPRouter.list_mcp_servers is not yet implemented.")
        raise NotImplementedError("MCPRouter.list_mcp_servers is not yet implemented.")

    async def query_mcp_tools(
        self, request: mcp_connection.QueryMCPToolsRequest, context: grpc.aio.ServicerContext
    ) -> mcp_connection.QueryMCPToolsResponse:
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("MCPRouter.query_mcp_tools is not yet implemented.")
        raise NotImplementedError("MCPRouter.query_mcp_tools is not yet implemented.")
