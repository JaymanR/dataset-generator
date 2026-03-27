import os
from enum import Enum
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

# Enums

class BackendType(str, Enum):
    LOCAL = "local"
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    HF_API = "hf_api"
    
class DeviceType(str, Enum):
    CPU = "cpu"
    CUDA = "cuda"
    MPS = "mps"
    
class GenerationConfig(BaseModel):
    """Parameters to configure LLM output"""
    
    temperature: float = Field(default=0.9, ge=0.0, le=2.0)
    max_new_tokens: int = Field(default=512, ge=64, le=4096)
    batch_size: int = Field(default=5, ge=1, le=50)
    total_records: int = Field(default=20, ge=1, le=10_000)
    top_p: float = Field(default=0.95, ge=0.0, le=1.0)
    
class LocalModelConfig(BaseModel):
    """Settings for running a local HF model."""
    
    model_id: str = "google/gemma-3-270m-it"
    device: DeviceType = DeviceType.CPU
    load_in_8bit: bool = False
    load_in_4bit: bool = False
    
class APIConfig(BaseModel):
    """Settings for external API backends."""
    
    openai_api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    anthropic_api_key: str = Field(default_factory=lambda: os.getenv("ANTHROPIC_API_KEY", ""))
    hf_api_token: str = Field(default_factory=lambda: os.getenv("HF_API_TOKEN", ""))
 
    # Model names used per API
    openai_model: str = "gpt-4o-mini"
    anthropic_model: str = "claude-haiku-4-5-20251001"
    hf_inference_model: str = "mistralai/Mistral-7B-Instruct-v0.2"
    
class ExportConfig(BaseModel):
    output_dir: str = "outputs"
    default_filename: str = "dataset"
    
class AppConfig(BaseModel):
    backend: BackendType = BackendType.OPENAI
    generation: GenerationConfig = Field(default_factory=GenerationConfig)
    local_model: LocalModelConfig = Field(default_factory=LocalModelConfig)
    api: APIConfig = Field(default_factory=APIConfig)
    export: ExportConfig = Field(default_factory=ExportConfig)
    
config = AppConfig()