# src/nodus/core/mcp/tools.py

# This file defines a catalog of mock tools for the MCP service.
# In a real-world scenario, these would be discovered from live microservices.

MOCK_TOOL_CATALOG = {
    "calculator": {
        "tool_id": "mcp-calculator-001",
        "name": "calculator",
        "description": "Performs basic arithmetic operations (add, subtract, multiply, divide).",
        "input_schema": {
            "type": "object",
            "properties": {
                "operation": {"type": "string", "enum": ["add", "subtract", "multiply", "divide"]},
                "operand1": {"type": "number"},
                "operand2": {"type": "number"},
            },
            "required": ["operation", "operand1", "operand2"],
        },
        "output_schema": {"type": "object", "properties": {"result": {"type": "number"}}},
    },
    "web_search": {
        "tool_id": "mcp-web_search-002",
        "name": "web_search",
        "description": "Searches the web for a given query and returns the top results.",
        "input_schema": {
            "type": "object",
            "properties": {"query": {"type": "string"}},
            "required": ["query"],
        },
        "output_schema": {"type": "object", "properties": {"results": {"type": "array", "items": {"type": "string"}}}} 
    }
}
