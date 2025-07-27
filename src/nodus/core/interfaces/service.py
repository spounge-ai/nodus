import grpc
import logging

from nodus.protos import svc, svc_grpc
from nodus.protos.nodes import execution
from nodus.protos.mcp import connection as mcp_connection

logger = logging.getLogger(__name__)

class NodusService(svc_grpc.NodusServiceServicer):
    def __init__(self):
        logger.info("NodusService initialized.")

    async def ExecuteNode(
        self, request: execution.ExecuteNodeRequest, context: grpc.aio.ServicerContext
    ) -> execution.ExecuteNodeResponse:
        logger.info(f"ExecuteNode called for node_id: {request.node_id}")
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("ExecuteNode is not yet implemented.")
        raise NotImplementedError("ExecuteNode is not yet implemented.")

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
        logger.info(f"RegisterMCPServer called for server_id: {request.server_id}")
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("RegisterMCPServer is not yet implemented.")
        raise NotImplementedError("RegisterMCPServer is not yet implemented.")

    async def ListMCPServers(
        self,
        request: mcp_connection.ListMCPServersRequest,
        context: grpc.aio.ServicerContext,
    ) -> mcp_connection.ListMCPServersResponse:
        logger.info("ListMCPServers called.")
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("ListMCPServers is not yet implemented.")
        raise NotImplementedError("ListMCPServers is not yet implemented.")

    async def QueryMCPTools(
        self,
        request: mcp_connection.QueryMCPToolsRequest,
        context: grpc.aio.ServicerContext,
    ) -> mcp_connection.QueryMCPToolsResponse:
        logger.info("QueryMCPTools called.")
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("QueryMCPTools is not yet implemented.")
        raise NotImplementedError("QueryMCPTools is not yet implemented.")

    async def CheckHealth(
        self, request: svc.CheckHealthRequest, context: grpc.aio.ServicerContext
    ) -> svc.CheckHealthResponse:
        logger.info(f"Health check requested for service: '{request.service or 'all'}'")
        return svc.CheckHealthResponse(status=svc.CheckHealthResponse.ServingStatus.SERVING_STATUS_SERVING)