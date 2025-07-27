# src/nodus/mock/auto_mock.py

MOCK_AUTONOMOUS_RESULT = {
    "objective_summary": "Successfully researched and compiled a report on the latest trends in renewable energy.",
    "final_output": {
        "report_title": "2025 Renewable Energy Trends",
        "key_findings": [
            "Solar power efficiency has increased by 15%.",
            "Wind turbine costs have decreased by 10%.",
            "Geothermal energy is gaining traction in new markets."
        ],
        "data_sources": [
            "market_analysis_api",
            "internal_research_db"
        ]
    },
    "iterations": 4,
    "total_tool_calls": 7,
    "agent_trajectory": [
        "Decomposed the main objective into sub-goals.",
        "Initiated research by querying the 'market_analysis_api'.",
        "Cross-referenced findings with the 'internal_research_db'.",
        "Synthesized the final report and summarized key findings."
    ]
}
