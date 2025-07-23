"""
Nodus Integrations - Protobuf services and types.
Auto-generated SDK module for microservice integration.
"""

from typing import Dict, Any
from spounge.nodus.v1.integrations.v1.llm_pb2 import llm_pb2
from spounge.nodus.v1.integrations.v1.llm_pb2_grpc import llm_pb2_grpc
from spounge.nodus.v1.integrations.v1.database_pb2 import database_pb2
from spounge.nodus.v1.integrations.v1.webhook_pb2 import webhook_pb2
from spounge.nodus.v1.integrations.v1.database_pb2_grpc import database_pb2_grpc
from spounge.nodus.v1.integrations.v1.api_pb2 import api_pb2
from spounge.nodus.v1.integrations.v1.webhook_pb2_grpc import webhook_pb2_grpc
from spounge.nodus.v1.integrations.v1.api_pb2_grpc import api_pb2_grpc

# Service stubs for integrations
SERVICES: Dict[str, Any] = {
    'llm': llm_pb2_grpc,
    'database': database_pb2_grpc,
    'webhook': webhook_pb2_grpc,
    'api': api_pb2_grpc,
}

# Message types for integrations  
TYPES: Dict[str, Any] = {
    'llm': llm_pb2,
    'database': database_pb2,
    'webhook': webhook_pb2,
    'api': api_pb2,
}

def get_service(name: str):
    """Get service stub by name."""
    return SERVICES.get(name)

def get_type(name: str):
    """Get message type by name.""" 
    return TYPES.get(name)

# Direct exports
llm = llm_pb2
llm = llm_pb2_grpc
database = database_pb2
webhook = webhook_pb2
database = database_pb2_grpc
api = api_pb2
webhook = webhook_pb2_grpc
api = api_pb2_grpc

__all__ = [
    "SERVICES", "TYPES", "get_service", "get_type",
    "llm",
    "llm",
    "database",
    "webhook",
    "database",
    "api",
    "webhook",
    "api",
]
