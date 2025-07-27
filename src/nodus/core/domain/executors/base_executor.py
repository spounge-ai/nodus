# src/nodus/core/domain/executors/base_executor.py
from abc import ABC, abstractmethod
import grpc
from nodus.protos import nodes

class BaseExecutor(ABC):
    @abstractmethod
    async def execute(
        self, request: nodes.execution.ExecuteNodeRequest, context: grpc.aio.ServicerContext
    ) -> nodes.execution.ExecuteNodeResponse:
        pass
