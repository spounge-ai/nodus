"""
Nodus Service - Protobuf services and types.
Auto-generated SDK module for microservice integration.
"""

from typing import Dict, Any
from spounge.nodus.v1.service.v1.service_pb2 import service_pb2
from spounge.nodus.v1.service.v1.service_pb2_grpc import service_pb2_grpc

# Service stubs for service
SERVICES: Dict[str, Any] = {
    'service': service_pb2_grpc,
}

# Message types for service  
TYPES: Dict[str, Any] = {
    'service': service_pb2,
}

def get_service(name: str):
    """Get service stub by name."""
    return SERVICES.get(name)

def get_type(name: str):
    """Get message type by name.""" 
    return TYPES.get(name)

# Direct exports
service = service_pb2
service = service_pb2_grpc

__all__ = [
    "SERVICES", "TYPES", "get_service", "get_type",
    "service",
    "service",
]
