"""
Nodus Mcp Protocol Buffer Aliases.
"""

# Imports
from spounge.nodus.v1.mcp.v1.connection_pb2 import connection_pb2
from spounge.nodus.v1.mcp.v1.connection_pb2_grpc import connection_pb2_grpc
from spounge.nodus.v1.mcp.v1.server_pb2 import server_pb2
from spounge.nodus.v1.mcp.v1.server_pb2_grpc import server_pb2_grpc
from spounge.nodus.v1.mcp.v1.tool_pb2 import tool_pb2
from spounge.nodus.v1.mcp.v1.tool_pb2_grpc import tool_pb2_grpc

# Aliases
connection = connection_pb2
connection_grpc = connection_pb2_grpc
server = server_pb2
server_grpc = server_pb2_grpc
tool = tool_pb2
tool_grpc = tool_pb2_grpc

# Exports
__all__ = [
    "connection",
    "connection_grpc",
    "server",
    "server_grpc",
    "tool",
    "tool_grpc",
]
