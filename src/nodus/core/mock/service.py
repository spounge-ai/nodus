# src/nodus/core/mock/service.py
import grpc
import logging
from concurrent import futures

from nodus.protos import (
    autonomous, autonomous_grpc,
    direct, direct_grpc,
    execution, execution_grpc,
    reasoning, reasoning_grpc,
    webhook, webhook_grpc
)
from nodus.core.mock.data import MOCK_NODE_DATA

logger = logging.getLogger(__name__)

class MockNodusService(
    autonomous_grpc.AutonomousServiceServicer,
    direct_grpc.DirectServiceServicer,
    execution_grpc.ExecutionServiceServicer,
    reasoning_grpc.ReasoningServiceServicer,
    webhook_grpc.WebhookServiceServicer
):
    def __init__(self):
        self.nodes = {}

    async def CreateAutonomousNode(self, request, context):
        node_id = f"auto_node_{len(self.nodes) + 1}"
        node_details = {
            "id": node_id,
            "name": request.name,
            "type": "autonomous",
            "data": MOCK_NODE_DATA["autonomous"]
        }
        self.nodes[node_id] = node_details
        logger.info(f"Created Autonomous Node: {node_details}")
        return autonomous.CreateNodeResponse(node_id=node_id, status="CREATED")

    async def CreateDirectNode(self, request, context):
        node_id = f"direct_node_{len(self.nodes) + 1}"
        node_details = {
            "id": node_id,
            "name": request.name,
            "type": "direct",
            "data": MOCK_NODE_DATA["direct"]
        }
        self.nodes[node_id] = node_details
        logger.info(f"Created Direct Node: {node_details}")
        return direct.CreateNodeResponse(node_id=node_id, status="CREATED")

    async def CreateExecutionNode(self, request, context):
        node_id = f"exec_node_{len(self.nodes) + 1}"
        node_details = {
            "id": node_id,
            "name": request.name,
            "type": "execution",
            "data": MOCK_NODE_DATA["execution"]
        }
        self.nodes[node_id] = node_details
        logger.info(f"Created Execution Node: {node_details}")
        return execution.CreateNodeResponse(node_id=node_id, status="CREATED")

    async def ExecuteNode(self, request, context):
        node_id = request.node_id
        if node_id not in self.nodes or self.nodes[node_id]["type"] != "execution":
            logger.warning(f"Execution failed: Node {node_id} not found or not an execution type.")
            await context.abort(grpc.StatusCode.NOT_FOUND, "Node not found or not an execution node.")
            return

        node_data = self.nodes[node_id]["data"]
        script_to_execute = node_data.get("script", "No script provided.")
        logger.info(f"Executing node {node_id} with script: {script_to_execute}")
        output = f"Executed script for {node_id}: '{script_to_execute}' with input: '{request.input_data}'"
        return execution.ExecuteNodeResponse(output=output, status="COMPLETED")

    async def CreateReasoningNode(self, request, context):
        node_id = f"reason_node_{len(self.nodes) + 1}"
        node_details = {
            "id": node_id,
            "name": request.name,
            "type": "reasoning",
            "data": MOCK_NODE_DATA["reasoning"]
        }
        self.nodes[node_id] = node_details
        logger.info(f"Created Reasoning Node: {node_details}")
        return reasoning.CreateNodeResponse(node_id=node_id, status="CREATED")

    async def CreateWebhookNode(self, request, context):
        node_id = f"webhook_node_{len(self.nodes) + 1}"
        node_details = {
            "id": node_id,
            "name": request.name,
            "type": "webhook",
            "data": MOCK_NODE_DATA["webhook"]
        }
        self.nodes[node_id] = node_details
        logger.info(f"Created Webhook Node: {node_details}")
        return webhook.CreateNodeResponse(node_id=node_id, status="CREATED")