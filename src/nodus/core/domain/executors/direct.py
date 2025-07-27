import grpc
import logging
from google.protobuf import any_pb2, struct_pb2
from nodus.protos.nodes import execution
from nodus.protos.common import types as common_types
from nodus.core.domain.executors.base_executor import BaseExecutor

logger = logging.getLogger(__name__)

class DirectExecutor(BaseExecutor):
    async def execute(
        self, request: execution.ExecuteNodeRequest, context: grpc.aio.ServicerContext
    ) -> execution.ExecuteNodeResponse:
        logger.info(f"Executing direct node: {request.node_id}")

        tool_params = request.direct_config.tool_parameters
        # In a real implementation, this would involve a call to the MCP client.
        # For now, we simulate a successful tool call.
        result_data = {
            "tool_name": request.direct_config.tool_name,
            "parameters": tool_params.items(),
            "result": {"status": "success", "output": "mock tool output"},
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
