"""
Nodus Protocol Buffer Client SDK.
Provides unified access to all Nodus microservices.
"""

from typing import Dict, Any, Optional, List
import grpc
from .nodes import SERVICES as NODES_SERVICES, TYPES as NODES_TYPES
from .service import SERVICES as SERVICE_SERVICES, TYPES as SERVICE_TYPES
from .integrations import SERVICES as INTEGRATIONS_SERVICES, TYPES as INTEGRATIONS_TYPES
from .common import SERVICES as COMMON_SERVICES, TYPES as COMMON_TYPES
from .mcp import SERVICES as MCP_SERVICES, TYPES as MCP_TYPES

class NodusClient:
    """Main client for Nodus microservices."""
    
    # All available services
    _SERVICES: Dict[str, Any] = {
    **NODES_SERVICES,
    **SERVICE_SERVICES,
    **INTEGRATIONS_SERVICES,
    **COMMON_SERVICES,
    **MCP_SERVICES,
    }
    
    # All available types
    _TYPES: Dict[str, Any] = {
    **NODES_TYPES,
    **SERVICE_TYPES,
    **INTEGRATIONS_TYPES,
    **COMMON_TYPES,
    **MCP_TYPES,
    }
    
    def __init__(self, channel: Optional[grpc.Channel] = None):
        """Initialize client with gRPC channel."""
        self.channel = channel
        self._service_instances = {}
    
    def service(self, name: str):
        """Get service stub instance."""
        if name not in self._service_instances:
            service_class = self._SERVICES.get(name)
            if not service_class:
                raise ValueError(f"Service '{name}' not found")
            if not self.channel:
                raise ValueError("gRPC channel required for service calls")
            self._service_instances[name] = service_class(self.channel)
        return self._service_instances[name]
    
    def type(self, name: str):
        """Get message type class."""
        type_class = self._TYPES.get(name)
        if not type_class:
            raise ValueError(f"Type '{name}' not found")
        return type_class
    
    @property
    def available_services(self) -> List[str]:
        """List all available service names."""
        return list(self._SERVICES.keys())
    
    @property  
    def available_types(self) -> List[str]:
        """List all available type names."""
        return list(self._TYPES.keys())

# Factory function
def create_client(endpoint: str, **kwargs) -> NodusClient:
    """Create Nodus client with gRPC channel."""
    channel = grpc.insecure_channel(endpoint, **kwargs)
    return NodusClient(channel)

__all__ = ["NodusClient", "create_client"]
