# src/nodus/core/mcp/client.py
import logging
from nodus.core.mcp.registry import MCPRegistry

logger = logging.getLogger(__name__)

class MCPClient:
    def __init__(self):
        self._registry = MCPRegistry()
        logger.info("MCPClient initialized.")

    def get_all_tools(self):
        return self._registry.list_tools()

    def get_tool_by_name(self, name: str):
        return self._registry.get_tool(name)
