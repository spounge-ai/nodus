# src/nodus/core/application/node_executor.py
import grpc
from nodus.protos.common import types_pb2 as common_types
from nodus.protos.nodes import execution
from nodus.core.domain.executors.direct import DirectExecutor
from nodus.core.domain.executors.reasoning import ReasoningExecutor
from nodus.core.domain.executors.autonomous import AutonomousExecutor
from nodus.core.domain.executors.webhook import WebhookExecutor

class NodeExecutor:
    def __init__(self):
        self._executors = {
            common_types.NODE_TYPE_DIRECT: DirectExecutor(),
            common_types.NODE_TYPE_REASONING: ReasoningExecutor(),
            common_types.NODE_TYPE_AUTONOMOUS: AutonomousExecutor(),
            common_types.NODE_TYPE_WEBHOOK: WebhookExecutor(),
        }

    async def execute(
        self, request: execution.ExecuteNodeRequest, context: grpc.aio.ServicerContext
    ) -> execution.ExecuteNodeResponse:
        executor = self._executors.get(request.node_type)
        if not executor:
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            context.set_details(f"Unsupported node type: {request.node_type}")
            return execution.ExecuteNodeResponse()
        return await executor.execute(request, context)
