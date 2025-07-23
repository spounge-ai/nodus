# src/nodus/core/server.py
import asyncio
import grpc
from concurrent import futures
import logging

# Import the service_grpc alias from nodus.protos
from nodus.protos import svc_grpc
from nodus.core.mock.service import MockNodusService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    mock_service = MockNodusService()

    # Only add the NodusServiceServicer (as defined in service.proto)
    svc_grpc.add_NodusServiceServicer_to_server(mock_service, server)

    listen_addr = '[::]:50052'
    server.add_insecure_port(listen_addr)
    logger.info(f"Starting Nodus Mock Server on {listen_addr} (consolidated service mode)")
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())