import grpc
import logging
from google.protobuf import any_pb2, struct_pb2
from nodus.protos.nodes import execution
from nodus.protos.common import types as common_types
from nodus.core.domain.executors.base_executor import BaseExecutor
from nodus.mock.auto_mock import MOCK_AUTONOMOUS_RESULT

logger = logging.getLogger(__name__)

class AutonomousExecutor(BaseExecutor):
    async def execute(
        self, request: execution.ExecuteNodeRequest, context: grpc.aio.ServicerContext
    ) -> execution.ExecuteNodeResponse:
        logger.info(f"Executing autonomous node: {request.node_id}")

        result_struct = struct_pb2.Struct()
        result_struct.update(MOCK_AUTONOMOUS_RESULT)

        any_result = any_pb2.Any()
        any_result.Pack(result_struct)

        return execution.ExecuteNodeResponse(
            execution_id=request.execution_id,
            node_id=request.node_id,
            status=common_types.EXECUTION_STATUS_COMPLETED,
            result_data=any_result,
        )
