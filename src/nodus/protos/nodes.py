"""
Nodus Nodes Protocol Buffer Aliases.
"""

# Imports
from spounge.nodus.v1.nodes.v1 import autonomous_pb2
from spounge.nodus.v1.nodes.v1 import autonomous_pb2_grpc
from spounge.nodus.v1.nodes.v1 import direct_pb2
from spounge.nodus.v1.nodes.v1 import direct_pb2_grpc
from spounge.nodus.v1.nodes.v1 import execution_pb2
from spounge.nodus.v1.nodes.v1 import execution_pb2_grpc
from spounge.nodus.v1.nodes.v1 import reasoning_pb2
from spounge.nodus.v1.nodes.v1 import reasoning_pb2_grpc
from spounge.nodus.v1.nodes.v1 import webhook_pb2
from spounge.nodus.v1.nodes.v1 import webhook_pb2_grpc

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
    "autonomous_pb2",
    "autonomous_grpc",
    "autonomous_pb2_grpc",
    "direct",
    "direct_pb2",
    "direct_grpc",
    "direct_pb2_grpc",
    "execution",
    "execution_pb2",
    "execution_grpc",
    "execution_pb2_grpc",
    "reasoning",
    "reasoning_pb2",
    "reasoning_grpc",
    "reasoning_pb2_grpc",
    "webhook",
    "webhook_pb2",
    "webhook_grpc",
    "webhook_pb2_grpc",
]
