"""
Nodus Common Protocol Buffer Aliases.
"""

# Imports
from spounge.nodus.v1.common.v1.auth_pb2 import auth_pb2
from spounge.nodus.v1.common.v1.auth_pb2_grpc import auth_pb2_grpc
from spounge.nodus.v1.common.v1.errors_pb2 import errors_pb2
from spounge.nodus.v1.common.v1.errors_pb2_grpc import errors_pb2_grpc
from spounge.nodus.v1.common.v1.resources_pb2 import resources_pb2
from spounge.nodus.v1.common.v1.resources_pb2_grpc import resources_pb2_grpc
from spounge.nodus.v1.common.v1.types_pb2 import types_pb2
from spounge.nodus.v1.common.v1.types_pb2_grpc import types_pb2_grpc

# Aliases
auth = auth_pb2
auth_grpc = auth_pb2_grpc
errors = errors_pb2
errors_grpc = errors_pb2_grpc
resources = resources_pb2
resources_grpc = resources_pb2_grpc
types = types_pb2
types_grpc = types_pb2_grpc

# Exports
__all__ = [
    "auth",
    "auth_grpc",
    "errors",
    "errors_grpc",
    "resources",
    "resources_grpc",
    "types",
    "types_grpc",
]
