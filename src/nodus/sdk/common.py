"""
Nodus Common - Protobuf services and types.
Auto-generated SDK module for microservice integration.
"""

from typing import Dict, Any
from spounge.nodus.v1.common.v1.auth_pb2 import auth_pb2
from spounge.nodus.v1.common.v1.auth_pb2_grpc import auth_pb2_grpc
from spounge.nodus.v1.common.v1.resources_pb2 import resources_pb2
from spounge.nodus.v1.common.v1.types_pb2_grpc import types_pb2_grpc
from spounge.nodus.v1.common.v1.errors_pb2 import errors_pb2
from spounge.nodus.v1.common.v1.resources_pb2_grpc import resources_pb2_grpc
from spounge.nodus.v1.common.v1.errors_pb2_grpc import errors_pb2_grpc
from spounge.nodus.v1.common.v1.types_pb2 import types_pb2

# Service stubs for common
SERVICES: Dict[str, Any] = {
    'auth': auth_pb2_grpc,
    'types': types_pb2_grpc,
    'resources': resources_pb2_grpc,
    'errors': errors_pb2_grpc,
}

# Message types for common  
TYPES: Dict[str, Any] = {
    'auth': auth_pb2,
    'resources': resources_pb2,
    'errors': errors_pb2,
    'types': types_pb2,
}

def get_service(name: str):
    """Get service stub by name."""
    return SERVICES.get(name)

def get_type(name: str):
    """Get message type by name.""" 
    return TYPES.get(name)

# Direct exports
auth = auth_pb2
auth = auth_pb2_grpc
resources = resources_pb2
types = types_pb2_grpc
errors = errors_pb2
resources = resources_pb2_grpc
errors = errors_pb2_grpc
types = types_pb2

__all__ = [
    "SERVICES", "TYPES", "get_service", "get_type",
    "auth",
    "auth",
    "resources",
    "types",
    "errors",
    "resources",
    "errors",
    "types",
]
