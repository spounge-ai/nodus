"""
Nodus Nodes - Protobuf services and types.
Auto-generated SDK module for microservice integration.
"""

from typing import Dict, Any
from spounge.nodus.v1.nodes.v1.reasoning_pb2 import reasoning_pb2
from spounge.nodus.v1.nodes.v1.execution_pb2_grpc import execution_pb2_grpc
from spounge.nodus.v1.nodes.v1.execution_pb2 import execution_pb2
from spounge.nodus.v1.nodes.v1.webhook_pb2 import webhook_pb2
from spounge.nodus.v1.nodes.v1.reasoning_pb2_grpc import reasoning_pb2_grpc
from spounge.nodus.v1.nodes.v1.autonomous_pb2_grpc import autonomous_pb2_grpc
from spounge.nodus.v1.nodes.v1.direct_pb2_grpc import direct_pb2_grpc
from spounge.nodus.v1.nodes.v1.direct_pb2 import direct_pb2
from spounge.nodus.v1.nodes.v1.webhook_pb2_grpc import webhook_pb2_grpc
from spounge.nodus.v1.nodes.v1.autonomous_pb2 import autonomous_pb2

# Service stubs for nodes
SERVICES: Dict[str, Any] = {
    'execution': execution_pb2_grpc,
    'reasoning': reasoning_pb2_grpc,
    'autonomous': autonomous_pb2_grpc,
    'direct': direct_pb2_grpc,
    'webhook': webhook_pb2_grpc,
}

# Message types for nodes  
TYPES: Dict[str, Any] = {
    'reasoning': reasoning_pb2,
    'execution': execution_pb2,
    'webhook': webhook_pb2,
    'direct': direct_pb2,
    'autonomous': autonomous_pb2,
}

def get_service(name: str):
    """Get service stub by name."""
    return SERVICES.get(name)

def get_type(name: str):
    """Get message type by name.""" 
    return TYPES.get(name)

# Direct exports
reasoning = reasoning_pb2
execution = execution_pb2_grpc
execution = execution_pb2
webhook = webhook_pb2
reasoning = reasoning_pb2_grpc
autonomous = autonomous_pb2_grpc
direct = direct_pb2_grpc
direct = direct_pb2
webhook = webhook_pb2_grpc
autonomous = autonomous_pb2

__all__ = [
    "SERVICES", "TYPES", "get_service", "get_type",
    "reasoning",
    "execution",
    "execution",
    "webhook",
    "reasoning",
    "autonomous",
    "direct",
    "direct",
    "webhook",
    "autonomous",
]
