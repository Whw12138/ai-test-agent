"""Optional LangChain-backed LLM adapter.

The rest of the project is deterministic by default so CI and demos work
without external API keys. This adapter is intentionally isolated.
"""

from __future__ import annotations

from ai_test_agent.config import Settings


class LLMUnavailableError(RuntimeError):
    """Raised when LLM mode is requested but dependencies or keys are missing."""


class LLMClient:
    def complete(self, prompt: str) -> str:
        raise NotImplementedError


class LangChainOpenAIClient(LLMClient):
    def __init__(self, settings: Settings) -> None:
        if not settings.llm_enabled:
            raise LLMUnavailableError("LLM mode requires AI_TEST_AGENT_USE_LLM=true and OPENAI_API_KEY.")
        try:
            from langchain_openai import ChatOpenAI
        except ImportError as exc:
            raise LLMUnavailableError("Install optional dependencies with: pip install -e .[llm]") from exc

        self._model = ChatOpenAI(
            model=settings.openai_model,
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
            temperature=0.1,
        )

    def complete(self, prompt: str) -> str:
        message = self._model.invoke(prompt)
        return str(message.content)
