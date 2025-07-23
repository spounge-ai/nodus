# src/nodus/core/mock/data.py

MOCK_NODE_DATA = {
    "autonomous": {
        "description": "Mock autonomous node for testing",
        "config": {"max_iterations": 10, "timeout": 30}
    },
    "direct": {
        "description": "Mock direct node for testing",
        "endpoint": "http://localhost:8080"
    },
    "execution": {
        "description": "Mock execution node for testing",
        "script": "print('Hello from execution node')"
    },
    "reasoning": {
        "description": "Mock reasoning node for testing",
        "model": "gpt-4",
        "prompt_template": "Analyze: {input}"
    },
    "webhook": {
        "description": "Mock webhook node for testing",
        "url": "https://api.example.com/webhook",
        "method": "POST"
    }
}