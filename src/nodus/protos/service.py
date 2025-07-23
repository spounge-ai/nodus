"""
Nodus Service Protocol Buffer Aliases.
"""

# Imports
from spounge.nodus.v1.service.v1.service_pb2 import service_pb2
from spounge.nodus.v1.service.v1.service_pb2_grpc import service_pb2_grpc

# Aliases
svc = service_pb2
svc_grpc = service_pb2_grpc

# Exports
__all__ = [
    "svc",
    "svc_grpc",
]
