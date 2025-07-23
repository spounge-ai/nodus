"""
Nodus Mcp - Protobuf services and types.
Auto-generated SDK module for microservice integration.
"""

from typing import Dict, Any
from spounge.nodus.v1.mcp.v1.connection_pb2_grpc import connection_pb2_grpc
from spounge.nodus.v1.mcp.v1.server_pb2_grpc import server_pb2_grpc
from spounge.nodus.v1.mcp.v1.tool_pb2 import tool_pb2
from spounge.nodus.v1.mcp.v1.connection_pb2 import connection_pb2
from spounge.nodus.v1.mcp.v1.server_pb2 import server_pb2
from spounge.nodus.v1.mcp.v1.tool_pb2_grpc import tool_pb2_grpc

# Service stubs for mcp
SERVICES: Dict[str, Any] = {
    'connection': connection_pb2_grpc,
    'server': server_pb2_grpc,
    'tool': tool_pb2_grpc,
}

# Message types for mcp  
TYPES: Dict[str, Any] = {
    'tool': tool_pb2,
    'connection': connection_pb2,
    'server': server_pb2,
}

def get_service(name: str):
    """Get service stub by name."""
    return SERVICES.get(name)

def get_type(name: str):
    """Get message type by name.""" 
    return TYPES.get(name)

# Direct exports
connection = connection_pb2_grpc
server = server_pb2_grpc
tool = tool_pb2
connection = connection_pb2
server = server_pb2
tool = tool_pb2_grpc

__all__ = [
    "SERVICES", "TYPES", "get_service", "get_type",
    "connection",
    "server",
    "tool",
    "connection",
    "server",
    "tool",
]
