# src/nodus/mock/reason_mock.py

MOCK_REASONING_RESULT = {
    "conclusion": "Based on a thorough analysis of the provided data, the primary recommendation is to proceed with the proposed strategy.",
    "confidence_score": 0.92,
    "reasoning_trace": [
        "Initial analysis of the user prompt identified the core problem.",
        "Invoked the 'data_fetcher' tool to gather relevant metrics.",
        "Analyzed the fetched data for key patterns and anomalies.",
        "Synthesized findings to formulate a conclusion.",
        "Final validation of the conclusion against initial requirements."
    ],
    "tool_calls_made": ["data_fetcher"]
}
