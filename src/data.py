
import uuid
from datetime import datetime, timedelta
from spounge.nodus import executeion_pb2 as execution



# Mock data for various tool results
MOCK_TOOL_RESULTS = {
    "weather_forecast": {
        "success": True,
        "result_data": {
            "city": "London",
            "temperature": "15°C",
            "condition": "Cloudy",
            "humidity": "80%",
            "wind_speed": "10 km/h"
        },
        "error_message": ""
    },
    "stock_price_lookup": {
        "success": True,
        "result_data": {
            "symbol": "GOOG",
            "price": 175.50,
            "currency": "USD",
            "timestamp": datetime.utcnow().isoformat() + 'Z'
        },
        "error_message": ""
    },
    "send_email": {
        "success": True,
        "result_data": {
            "status": "Email sent successfully",
            "recipient": "user@example.com"
        },
        "error_message": ""
    },
    "invalid_tool": {
        "success": False,
        "result_data": {},
        "error_message": "Tool not found or not supported."
    },
    "failed_tool": {
        "success": False,
        "result_data": {},
        "error_message": "Simulated tool execution failure due to external service error."
    }
}

# Mock node configurations (can be expanded)
MOCK_NODE_CONFIGS = {
    "node-weather-1": {
        "mcp_server_id": "mock-mcp-server-1",
        "tool_name": "weather_forecast",
        "tool_parameters": {
            "location": "London"
        }
    },
    "node-stock-1": {
        "mcp_server_id": "mock-mcp-server-2",
        "tool_name": "stock_price_lookup",
        "tool_parameters": {
            "symbol": "GOOG"
        }
    },
    "node-email-1": {
        "mcp_server_id": "mock-mcp-server-3",
        "tool_name": "send_email",
        "tool_parameters": {
            "to": "user@example.com",
            "subject": "Test Email",
            "body": "This is a test email from the node execution."
        }
    },
    "node-fail-1": {
        "mcp_server_id": "mock-mcp-server-4",
        "tool_name": "failed_tool",
        "tool_parameters": {}
    },
    "node-unknown-tool": {
        "mcp_server_id": "mock-mcp-server-5",
        "tool_name": "non_existent_tool",
        "tool_parameters": {}
    }
}

# Helper function to generate a unique execution ID
def generate_execution_id():
    return f"exec-{uuid.uuid4()}"

# Helper function to get current timestamp in RFC 3339 format
def get_current_timestamp():
    return datetime.utcnow().isoformat() + 'Z'
