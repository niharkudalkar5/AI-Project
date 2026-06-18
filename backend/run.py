"""
Standalone Local LLM Workspace
Runtime Configuration Module
"""
from app.config import Settings

# This module provides runtime configuration for all services
# Configuration can be set via:
# 1. Environment variables
# 2. .env file
# 3. Direct instantiation

__all__ = ["Settings"]
