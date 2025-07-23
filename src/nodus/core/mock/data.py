# src/nodus/core/mock/data.py

MOCK_NODE_DATA = {
    "direct": {
        "description": "Direct tool execution completed",
        "tool_name": "mock_calculator",
        "result": {
            "calculation": "2 + 2 = 4",
            "operation_type": "addition",
            "success": True
        },
        "execution_details": {
            "tool_calls": 1,
            "processing_time_ms": 150,
            "cache_hit": False
        }
    },
    "reasoning": {
        "description": "Reasoning task completed with chain of thought",
        "model": "mock-llm-v1",
        "reasoning_steps": [
            "Analyzed the input problem",
            "Considered multiple approaches", 
            "Selected optimal solution path",
            "Generated final response"
        ],
        "result": {
            "conclusion": "Based on the analysis, the recommended approach is X",
            "confidence": 0.87,
            "supporting_evidence": ["fact1", "fact2", "fact3"]
        },
        "token_usage": {
            "input_tokens": 450,
            "output_tokens": 230,
            "total_tokens": 680
        }
    },
    "autonomous": {
        "description": "Autonomous agent task completed",
        "agent_type": "react",
        "iterations": 3,
        "goals_achieved": ["primary_goal", "secondary_goal"],
        "actions_taken": [
            {"step": 1, "action": "analyze_environment", "result": "success"},
            {"step": 2, "action": "execute_plan", "result": "partial_success"}, 
            {"step": 3, "action": "refine_approach", "result": "success"}
        ],
        "final_state": {
            "status": "goal_achieved",
            "completion_percentage": 95,
            "remaining_tasks": []
        },
        "resource_usage": {
            "llm_calls": 8,
            "tool_invocations": 12,
            "memory_updates": 5
        }
    },
    "webhook": {
        "description": "Webhook callback processed",
        "webhook_id": "wh_12345",
        "payload_received": True,
        "validation_status": "passed",
        "processed_data": {
            "event_type": "user_action",
            "timestamp": "2024-01-15T10:30:00Z",
            "user_id": "user_789",
            "action_details": {
                "type": "button_click",
                "element_id": "submit_btn",
                "page": "/checkout"
            }
        },
        "response_sent": {
            "status_code": 200,
            "message": "Webhook processed successfully",
            "processing_time_ms": 85
        }
    }
}

MOCK_EXECUTION_SCENARIOS = {
    "success": {
        "probability": 0.8,
        "execution_time_range": (1, 4),
        "confidence_range": (0.85, 0.98)
    },
    "partial_success": {
        "probability": 0.15,
        "execution_time_range": (2, 6),
        "confidence_range": (0.60, 0.84),
        "warnings": ["minor_issue_detected", "fallback_used"]
    },
    "failure": {
        "probability": 0.05,
        "execution_time_range": (0.5, 2),
        "error_types": ["timeout", "validation_error", "external_service_unavailable"]
    }
}

MOCK_TOOLS_CATALOG = {
    "calculator": {
        "category": "computation",
        "description": "Performs mathematical operations",
        "operations": ["add", "subtract", "multiply", "divide", "power", "sqrt"]
    },
    "data_fetcher": {
        "category": "data_access", 
        "description": "Retrieves data from various sources",
        "sources": ["database", "api", "file_system", "cache"]
    },
    "text_analyzer": {
        "category": "analysis",
        "description": "Analyzes text content for insights",
        "features": ["sentiment", "entities", "keywords", "summary"]
    },
    "web_scraper": {
        "category": "web_browser",
        "description": "Extracts content from web pages",
        "capabilities": ["html_parsing", "javascript_execution", "screenshot"]
    },
    "email_sender": {
        "category": "communication",
        "description": "Sends emails through various providers",
        "providers": ["smtp", "sendgrid", "ses", "mailgun"]
    }
}