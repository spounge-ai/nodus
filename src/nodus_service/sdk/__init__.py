"""
Nodus Protocol Buffer SDK.
Modern microservice client library following July 2025 best practices.
"""

from .client import NodusClient, create_client
from . import nodes
from . import service
from . import integrations
from . import common
from . import mcp

__version__ = "1.0.0"
__all__ = ["NodusClient", "create_client"] + ['nodes', 'service', 'integrations', 'common', 'mcp']
