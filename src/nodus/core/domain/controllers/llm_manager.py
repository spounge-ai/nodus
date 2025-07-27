# src/nodus/core/domain/executors/llm_manager.py
import logging
from langchain_openai import ChatOpenAI
from nodus.protos import integrations
from nodus.core.integrations.llm.gemini_provider import GeminiLLMProvider
from nodus.core.integrations.polykey_client import PolykeyClient

logger = logging.getLogger(__name__)

class LLMManager:
    def __init__(self):
        self.polykey_client = PolykeyClient()
        self.llm_providers = {
            integrations.llm.LLM_PROVIDER_OPENAI: lambda config: ChatOpenAI(model=config.model_name, temperature=config.model_parameters.temperature if config.HasField("model_parameters") and config.model_parameters.HasField("temperature") else 0.7),
            integrations.llm.LLM_PROVIDER_GOOGLE: lambda config: GeminiLLMProvider(self.polykey_client).get_llm(config),
            # Add other LLM providers here as needed
        }

    def get_llm(self, llm_config: integrations.llm.LLMConfiguration):
        llm_provider_func = self.llm_providers.get(llm_config.provider)

        if not llm_provider_func:
            raise ValueError(f"Unsupported LLM provider: {llm_config.provider}")

        return llm_provider_func(llm_config)
