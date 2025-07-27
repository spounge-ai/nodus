# src/nodus/core/integrations/llm/gemini_provider.py
import logging
from langchain_google_genai import ChatGoogleGenerativeAI
from nodus.protos import integrations

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class GeminiLLMProvider:
    def __init__(self, polykey_client):
        self.polykey_client = polykey_client

    def get_llm(self, llm_config: integrations.llm.LLMConfiguration, llm_parameters: integrations.llm.LLMParameters = None):
        api_key = self.polykey_client.get_credential(llm_config.credential_id)
        if not api_key:
            raise ValueError(f"API key not found for credential_id: {llm_config.credential_id}")

        temperature = 0.7 # Default value
        if llm_parameters is not None:
            temperature = llm_parameters.temperature

        logger.info(f"Initializing Gemini LLM with model: {llm_config.model_name}")
        return ChatGoogleGenerativeAI(model=llm_config.model_name, google_api_key=api_key, temperature=temperature)
