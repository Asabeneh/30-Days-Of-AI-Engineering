import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Load .env from repo root or studyspark folder
for candidate in (
    Path(__file__).resolve().parents[3] / ".env",
    Path(__file__).resolve().parents[2] / ".env",
):
    if candidate.exists():
        load_dotenv(candidate)
        break
else:
    load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Environment-based configuration for StudySpark."""

    llm_provider: str = os.getenv("LLM_PROVIDER", "mock")
    openai_api_key: str | None = os.getenv("OPENAI_API_KEY")
    openai_model: str = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
    anthropic_api_key: str | None = os.getenv("ANTHROPIC_API_KEY")
    anthropic_model: str = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")
    request_timeout_seconds: float = float(os.getenv("REQUEST_TIMEOUT_SECONDS", "30"))


settings = Settings()
