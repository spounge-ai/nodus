# src/nodus/core/domain/executors/base_executor.py
from abc import ABC, abstractmethod
import grpc
from nodus.protos.nodes import execution

class BaseExecutor(ABC):
    @abstractmethod
    async def execute(
        self, request: execution.ExecuteNodeRequest, context: grpc.aio.ServicerContext
    ) -> execution.ExecuteNodeResponse:
        pass
