# src/nodus/core/domain/controllers/llm_manager.py
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
            integrations.llm.LLM_PROVIDER_OPENAI: lambda config, params: ChatOpenAI(model=config.model_name, temperature=params.temperature if params is not None else 0.7),
            integrations.llm.LLM_PROVIDER_GOOGLE: lambda config, params: GeminiLLMProvider(self.polykey_client).get_llm(config, params),
            # Add other LLM providers here as needed
        }

    def get_llm(self, llm_config: integrations.llm.LLMConfiguration, llm_parameters: integrations.llm.LLMParameters = None):
        llm_provider_func = self.llm_providers.get(llm_config.provider)

        if not llm_provider_func:
            raise ValueError(f"Unsupported LLM provider: {llm_config.provider}")

        logger.debug(f"LLMManager.get_llm: llm_config={llm_config}, llm_parameters={llm_parameters}")
        return llm_provider_func(llm_config, llm_parameters)
