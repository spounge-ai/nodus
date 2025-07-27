# src/nodus/core/integrations/llm/gemini_provider.py
import os
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from nodus.protos.integrations import llm_pb2 as llm_protos

logger = logging.getLogger(__name__)

class GeminiLLMProvider:
    def __init__(self, polykey_client):
        self.polykey_client = polykey_client

    def get_llm(self, llm_config: llm_protos.LLMConfiguration):
        api_key = self.polykey_client.get_credential(llm_config.credential_id)
        if not api_key:
            raise ValueError(f"API key not found for credential_id: {llm_config.credential_id}")

        # Extract parameters from llm_config.model_parameters if available
        # For simplicity, using default temperature for now
        temperature = 0.7 # Default value
        if llm_config.HasField("model_parameters"):
            if llm_config.model_parameters.HasField("temperature"):
                temperature = llm_config.model_parameters.temperature

        logger.info(f"Initializing Gemini LLM with model: {llm_config.model_name}")
        return ChatGoogleGenerativeAI(model=llm_config.model_name, google_api_key=api_key, temperature=temperature)
