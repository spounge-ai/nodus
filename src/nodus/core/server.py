# src/nodus/core/server.py
import asyncio
import grpc
from concurrent import futures
import logging

from nodus.protos import (
    autonomous_grpc,
    direct_grpc,
    execution_grpc,
    reasoning_grpc,
    webhook_grpc
)
from nodus.core.mock.service import MockNodusService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    mock_service = MockNodusService()

    autonomous_grpc.add_AutonomousServiceServicer_to_server(mock_service, server)
    direct_grpc.add_DirectServiceServicer_to_server(mock_service, server)
    execution_grpc.add_ExecutionServiceServicer_to_server(mock_service, server)
    reasoning_grpc.add_ReasoningServiceServicer_to_server(mock_service, server)
    webhook_grpc.add_WebhookServiceServicer_to_server(mock_service, server)

    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    logger.info(f"Starting Nodus Mock Server on {listen_addr}")
    await server.start()
    await server.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(serve())