import grpc
import logging

from nodus.protos import mcp
from nodus.protos.mcp.v1 import connection_pb2 as mcp_connection
from nodus.core.mcp.client import MCPClient

logger = logging.getLogger(__name__)


class MCPRouter:
    def __init__(self):
        self.mcp_client = MCPClient()

    async def register_mcp_server(
        self, request: mcp_connection.RegisterMCPServerRequest, context: grpc.aio.ServicerContext
    ) -> mcp_connection.RegisterMCPServerResponse:
        logger.warning("MCPRouter.register_mcp_server is a mock implementation.")
        return mcp.connection.RegisterMCPServerResponse(success=True, server_id=request.server_id)

    async def list_mcp_servers(
        self, request: mcp_connection.ListMCPServersRequest, context: grpc.aio.ServicerContext
    ) -> mcp_connection.ListMCPServersResponse:
        logger.warning("MCPRouter.list_mcp_servers is a mock implementation.")
        return mcp.connection.ListMCPServersResponse(servers=[], total_servers=0)

    async def query_mcp_tools(
        self, request: mcp_connection.QueryMCPToolsRequest, context: grpc.aio.ServicerContext
    ) -> mcp_connection.QueryMCPToolsResponse:
        logger.info("Querying for tools using the MCPClient.")
        tools = self.mcp_client.get_all_tools()
        return mcp.connection.QueryMCPToolsResponse(tools=tools, total_matches=len(tools))
