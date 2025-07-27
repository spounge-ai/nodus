# src/nodus/core/mcp/discovery.py
import logging
from nodus.core.mcp.tools import MOCK_TOOL_CATALOG

logger = logging.getLogger(__name__)

class ToolDiscoveryService:
    def __init__(self):
        self._tool_catalog = MOCK_TOOL_CATALOG
        logger.info(f"ToolDiscoveryService initialized with {len(self._tool_catalog)} mock tools.")

    def get_all_tools(self):
        return list(self._tool_catalog.values())

    def get_tool_by_name(self, name: str):
        return self._tool_catalog.get(name)
