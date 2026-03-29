from enum import Enum
import os
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel

load_dotenv()


class APIProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    HUGGINGFACE = "huggingface"


class APIModelConfig(BaseModel):
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


def initialize_clients():
    """Initialize and return clients"""

    anthropic_url = "https://api.anthropic.com/v1/"
    gemini_url = "https://generativelanguage.googleapis.com/v1beta/openai/"

    openai_key = os.getenv("OPENAI_API_KEY")
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    google_key = os.getenv("GOOGLE_API_KEY")

    clients = {}

    if openai_key:
        clients["openai"] = OpenAI(api_key=openai_key)
    else:
        raise ValueError("OPENAI_API_KEY NOT SET")
    if anthropic_key:
        clients["anthropic"] = OpenAI(api_key=anthropic_key, base_url=anthropic_url)
    else:
        raise ValueError("ANTHROPIC_API_KEY NOT SET")
    if google_key:
        clients["google"] = OpenAI(api_key=google_key, base_url=gemini_url)
    else:
        raise ValueError("GOOGLE_API_KEY NOT SET")

    return clients
