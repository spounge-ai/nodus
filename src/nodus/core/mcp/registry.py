# src/nodus/core/mcp/registry.py
import logging
from nodus.core.mcp.discovery import ToolDiscoveryService

logger = logging.getLogger(__name__)

class MCPRegistry:
    def __init__(self):
        self._discovery_service = ToolDiscoveryService()
        logger.info("MCPRegistry initialized.")

    def list_tools(self):
        return self._discovery_service.get_all_tools()

    def get_tool(self, name: str):
        return self._discovery_service.get_tool_by_name(name)
