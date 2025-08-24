# src/nodus/core/server.py
import asyncio
import grpc
from concurrent import futures
import logging
import argparse

from nodus.protos.service import svc_grpc
from nodus.core.interfaces.service import NodusService
from nodus.mock.service import MockNodusService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def serve(mock: bool = False):
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))
    if mock:
        service = MockNodusService()
        logger.info("Using MockNodusService")
    else:
        service = NodusService()
        logger.info("Using NodusService")

    svc_grpc.add_NodusServiceServicer_to_server(service, server)

    listen_addr = '[::]:50052'
    server.add_insecure_port(listen_addr)
    logger.info(f"Starting Nodus Server on {listen_addr}")
    await server.start()
    await server.wait_for_termination() 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--mock", action="store_true", help="Run the server with the mock service.")
    args = parser.parse_args()
    asyncio.run(serve(args.mock))