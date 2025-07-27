# src/nodus/core/server.py
import asyncio
import grpc
from concurrent import futures
import logging

from nodus.protos import svc_grpc
from nodus.core.interfaces.service import NodusService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def serve():
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    service = NodusService()

    svc_grpc.add_NodusServiceServicer_to_server(service, server)

    listen_addr = '[::]:50052'
    server.add_insecure_port(listen_addr)
    logger.info(f"Starting Nodus Server on {listen_addr}")
    await server.start()
    await server.wait_for_termination() 

if __name__ == '__main__':
    asyncio.run(serve())