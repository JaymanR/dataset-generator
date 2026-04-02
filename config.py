from dataclasses import dataclass
from enum import Enum
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


class APIProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    HUGGINGFACE = "huggingface"


@dataclass(frozen=True)
class APIModelConfig:
    provider: APIProvider
    model_id: str

class Models:
    """Model presets."""

    # OpenAI
    GPT_5_NANO = APIModelConfig(provider=APIProvider.OPENAI, model_id="gpt-5-nano")
    GPT_5_4_MINI = APIModelConfig(provider=APIProvider.OPENAI, model_id="gpt-5.4-mini")

    # Anthropic
    CLAUDE_HAIKU_4_5 = APIModelConfig(
        provider=APIProvider.ANTHROPIC, model_id="claude-haiku-4-5"
    )

    # Google
    GEMINI_2_5_FLASH_LITE = APIModelConfig(
        provider=APIProvider.GOOGLE, model_id="gemini-2.5-flash-lite"
    )

    # HuggingFace Serverless
    QWEN3_8B = APIModelConfig(
        provider=APIProvider.HUGGINGFACE, model_id="Qwen/Qwen3-8B"
    )
    QWEN3_4B = APIModelConfig(
        provider=APIProvider.HUGGINGFACE, model_id="Qwen/Qwen3-4B"
    )


def initialize_client(model_config: APIModelConfig) -> OpenAI:
    """Create an API client for the selected provider only."""

    anthropic_url = "https://api.anthropic.com/v1/"
    gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
    huggingface_url = "https://router.huggingface.co/v1"

    if model_config.provider == APIProvider.OPENAI:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is not set")
        return OpenAI(api_key=api_key)

    if model_config.provider == APIProvider.ANTHROPIC:
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY is not set")
        return OpenAI(api_key=api_key, base_url=anthropic_url)

    if model_config.provider == APIProvider.GOOGLE:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY is not set")
        return OpenAI(api_key=api_key, base_url=gemini_url)

    if model_config.provider == APIProvider.HUGGINGFACE:
        api_key = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_API_KEY")
        if not api_key:
            raise ValueError("HF_TOKEN or HUGGINGFACE_API_KEY is not set")
        return OpenAI(api_key=api_key, base_url=huggingface_url)

    raise ValueError(f"Unsupported provider: {model_config.provider}")
