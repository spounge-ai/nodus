"""
Nodus Integrations Protocol Buffer Aliases.
"""

# Imports
from spounge.nodus.v1.integrations.v1 import api_pb2
from spounge.nodus.v1.integrations.v1 import api_pb2_grpc
from spounge.nodus.v1.integrations.v1 import database_pb2
from spounge.nodus.v1.integrations.v1 import database_pb2_grpc
from spounge.nodus.v1.integrations.v1 import llm_pb2
from spounge.nodus.v1.integrations.v1 import llm_pb2_grpc
from spounge.nodus.v1.integrations.v1 import webhook_pb2
from spounge.nodus.v1.integrations.v1 import webhook_pb2_grpc

# Aliases
api = api_pb2
api_grpc = api_pb2_grpc
database = database_pb2
database_grpc = database_pb2_grpc
llm = llm_pb2
llm_grpc = llm_pb2_grpc
webhook = webhook_pb2
webhook_grpc = webhook_pb2_grpc

# Exports
__all__ = [
    "api",
    "api_pb2",
    "api_grpc",
    "api_pb2_grpc",
    "database",
    "database_pb2",
    "database_grpc",
    "database_pb2_grpc",
    "llm",
    "llm_pb2",
    "llm_grpc",
    "llm_pb2_grpc",
    "webhook",
    "webhook_pb2",
    "webhook_grpc",
    "webhook_pb2_grpc",
]
