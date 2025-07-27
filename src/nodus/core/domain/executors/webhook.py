import grpc
import logging
import asyncio
from google.protobuf import any_pb2, struct_pb2
from nodus.protos.nodes import execution
from nodus.protos.common import types as common_types
from nodus.core.domain.executors.base_executor import BaseExecutor

logger = logging.getLogger(__name__)

class WebhookExecutor(BaseExecutor):
    async def execute(
        self, request: execution.ExecuteNodeRequest, context: grpc.aio.ServicerContext
    ) -> execution.ExecuteNodeResponse:
        logger.info(f"Executing webhook node: {request.node_id}")

        # In a real implementation, this would involve a webhook dispatcher
        # that waits for an incoming callback.
        await asyncio.sleep(2)  # Simulate waiting for a webhook.

        result_data = {
            "listen_id": request.webhook_config.listen_id,
            "received_data": {"status": "success", "payload": {"message": "mock webhook callback"}},
        }

        result_struct = struct_pb2.Struct()
        result_struct.update(result_data)

        any_result = any_pb2.Any()
        any_result.Pack(result_struct)

        return execution.ExecuteNodeResponse(
            execution_id=request.execution_id,
            node_id=request.node_id,
            status=common_types.EXECUTION_STATUS_COMPLETED,
            result_data=any_result,
        )
