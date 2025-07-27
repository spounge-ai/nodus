# src/nodus/core/application/node_executor.py
import grpc
import logging

from nodus.protos import common
from nodus.protos import execution
from nodus.core.domain.executors.autonomous import AutonomousExecutor
from nodus.core.domain.executors.direct import DirectExecutor
from nodus.core.domain.executors.reasoning import ReasoningExecutor
from nodus.core.domain.executors.webhook import WebhookExecutor
from nodus.core.mcp.client import MCPClient
from nodus.core.domain.controllers.llm_manager import LLMManager

logger = logging.getLogger(__name__)


class NodeExecutor:
    def __init__(self):
        mcp_client = MCPClient()
        llm_manager = LLMManager()
        self._executors = {
            common.types.NodeType.NODE_TYPE_DIRECT: DirectExecutor(),
            common.types.NodeType.NODE_TYPE_REASONING: ReasoningExecutor(mcp_client=mcp_client, llm_manager=llm_manager),
            common.types.NodeType.NODE_TYPE_AUTONOMOUS: AutonomousExecutor(mcp_client=mcp_client, llm_manager=llm_manager),
            common.types.NodeType.NODE_TYPE_WEBHOOK: WebhookExecutor(),
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
