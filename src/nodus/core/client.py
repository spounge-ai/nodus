# src/nodus/core/client.py
import asyncio
import grpc
import logging

from nodus.protos import (
    autonomous, autonomous_grpc,
    direct, direct_grpc,
    execution, execution_grpc,
    reasoning, reasoning_grpc,
    webhook, webhook_grpc
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        logger.info("Connected to gRPC server.")

        auto_stub = autonomous_grpc.AutonomousServiceStub(channel)
        auto_request = autonomous.CreateNodeRequest(name="MyAutonomousNode")
        auto_response = await auto_stub.CreateAutonomousNode(auto_request)
        logger.info(f"Created Autonomous Node: ID={auto_response.node_id}, Status={auto_response.status}")

        direct_stub = direct_grpc.DirectServiceStub(channel)
        direct_request = direct.CreateNodeRequest(name="MyDirectNode")
        direct_response = await direct_stub.CreateDirectNode(direct_request)
        logger.info(f"Created Direct Node: ID={direct_response.node_id}, Status={direct_response.status}")

        exec_stub = execution_grpc.ExecutionServiceStub(channel)
        exec_request = execution.CreateNodeRequest(name="MyExecutionNode")
        exec_response = await exec_stub.CreateExecutionNode(exec_request)
        execution_node_id = exec_response.node_id
        logger.info(f"Created Execution Node: ID={execution_node_id}, Status={exec_response.status}")

        reason_stub = reasoning_grpc.ReasoningServiceStub(channel)
        reason_request = reasoning.CreateNodeRequest(name="MyReasoningNode")
        reason_response = await reason_stub.CreateReasoningNode(reason_request)
        logger.info(f"Created Reasoning Node: ID={reason_response.node_id}, Status={reason_response.status}")

        webhook_stub = webhook_grpc.WebhookServiceStub(channel)
        webhook_request = webhook.CreateNodeRequest(name="MyWebhookNode")
        webhook_response = await webhook_stub.CreateWebhookNode(webhook_request)
        logger.info(f"Created Webhook Node: ID={webhook_response.node_id}, Status={webhook_response.status}")

        if execution_node_id:
            logger.info(f"Attempting to execute Execution Node: {execution_node_id}")
            execute_request = execution.ExecuteNodeRequest(
                node_id=execution_node_id,
                input_data="This is some input for the execution."
            )
            try:
                execute_response = await exec_stub.ExecuteNode(execute_request)
                logger.info(f"Execution Node Output: {execute_response.output}")
                logger.info(f"Execution Status: {execute_response.status}")
            except grpc.aio.AioRpcError as e:
                logger.error(f"Error executing node {execution_node_id}: {e.code().name} - {e.details()}")
        else:
            logger.warning("No execution node ID available for execution test.")

if __name__ == '__main__':
    asyncio.run(main())