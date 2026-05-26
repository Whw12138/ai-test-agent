"""Runtime configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    use_llm: bool = _as_bool(os.getenv("AI_TEST_AGENT_USE_LLM"), False)
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_base_url: str = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    output_dir: Path = Path(os.getenv("AI_TEST_AGENT_OUTPUT_DIR", "runs/demo"))
    target_base_url: str = os.getenv("AI_TEST_AGENT_TARGET_BASE_URL", "http://testserver")

    @property
    def llm_enabled(self) -> bool:
        return self.use_llm and bool(self.openai_api_key)


settings = Settings()
