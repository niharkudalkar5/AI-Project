"""Application configuration and environment settings."""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings."""
    
    # App settings
    APP_NAME: str = "Standalone Local LLM Workspace"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # API settings
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("API_PORT", "8000"))
    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000")
    
    # Frontend settings
    FRONTEND_PORT: int = int(os.getenv("FRONTEND_PORT", "3000"))
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    
    # LLM Connector settings
    LLM_ADAPTER: str = os.getenv("LLM_ADAPTER", "generic")  # generic, ollama, or custom
    LLM_ENDPOINT: str = os.getenv("LLM_ENDPOINT", "http://localhost:11434")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "mistral")
    LLM_TIMEOUT: int = int(os.getenv("LLM_TIMEOUT", "300"))
    LLM_CONTEXT_LIMIT: int = int(os.getenv("LLM_CONTEXT_LIMIT", "4096"))
    
    # Workspace settings
    WORKSPACE_ROOT: str = os.getenv("WORKSPACE_ROOT", "workspace")
    MODULES_DIR: str = os.path.join(WORKSPACE_ROOT, "modules")
    INDEXES_DIR: str = os.path.join(WORKSPACE_ROOT, "indexes")
    MEMORY_DIR: str = os.path.join(WORKSPACE_ROOT, "memory")
    LOGS_DIR: str = os.path.join(WORKSPACE_ROOT, "logs")
    PATCHES_DIR: str = os.path.join(WORKSPACE_ROOT, "patches")
    
    # Feature flags
    ENABLE_OLLAMA_ADAPTER: bool = True
    ENABLE_CODE_REVIEW: bool = True
    ENABLE_SAFE_PATCHING: bool = True
    ENABLE_EMBEDDINGS: bool = True
    
    class Config:
        env_file = str(Path(__file__).resolve().parent.parent / ".env")
        case_sensitive = True

settings = Settings()
