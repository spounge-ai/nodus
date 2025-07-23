"""
Nodus Nodes Protocol Buffer Aliases.
"""

# Imports
from spounge.nodus.v1.nodes.v1.autonomous_pb2 import autonomous_pb2
from spounge.nodus.v1.nodes.v1.autonomous_pb2_grpc import autonomous_pb2_grpc
from spounge.nodus.v1.nodes.v1.direct_pb2 import direct_pb2
from spounge.nodus.v1.nodes.v1.direct_pb2_grpc import direct_pb2_grpc
from spounge.nodus.v1.nodes.v1.execution_pb2 import execution_pb2
from spounge.nodus.v1.nodes.v1.execution_pb2_grpc import execution_pb2_grpc
from spounge.nodus.v1.nodes.v1.reasoning_pb2 import reasoning_pb2
from spounge.nodus.v1.nodes.v1.reasoning_pb2_grpc import reasoning_pb2_grpc
from spounge.nodus.v1.nodes.v1.webhook_pb2 import webhook_pb2
from spounge.nodus.v1.nodes.v1.webhook_pb2_grpc import webhook_pb2_grpc

# Aliases
autonomous = autonomous_pb2
autonomous_grpc = autonomous_pb2_grpc
direct = direct_pb2
direct_grpc = direct_pb2_grpc
execution = execution_pb2
execution_grpc = execution_pb2_grpc
reasoning = reasoning_pb2
reasoning_grpc = reasoning_pb2_grpc
webhook = webhook_pb2
webhook_grpc = webhook_pb2_grpc

# Exports
__all__ = [
    "autonomous",
    "autonomous_grpc",
    "direct",
    "direct_grpc",
    "execution",
    "execution_grpc",
    "reasoning",
    "reasoning_grpc",
    "webhook",
    "webhook_grpc",
]
