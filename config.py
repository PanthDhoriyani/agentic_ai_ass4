"""
Configuration module for Assignment 4: Multi-Agent Systems & Collaboration.
Configures LLM endpoints, AutoGen model clients, and project-wide parameters.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load .env from current directory or parent directories
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    # Fallback to check jury .env
    jury_env = Path("d:/anything/agentic ai/agentic_ai_ jury_1/.env")
    if jury_env.exists():
        load_dotenv(dotenv_path=jury_env)
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "openai/gpt-oss-120b")
FAST_MODEL = os.getenv("FAST_MODEL", "openai/gpt-oss-20b")
BASE_URL = "https://api.groq.com/openai/v1"

# Directory paths
BASE_DIR = Path(__file__).resolve().parent
LOGS_DIR = BASE_DIR / "logs"
ARTIFACTS_DIR = BASE_DIR / "artifacts"

LOGS_DIR.mkdir(exist_ok=True)
ARTIFACTS_DIR.mkdir(exist_ok=True)


def get_model_client(model: str = DEFAULT_MODEL, temperature: float = 0.2) -> OpenAIChatCompletionClient:
    """
    Returns an AutoGen OpenAI-compatible chat completion client configured for Groq.
    """
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is not set in environment or .env file.")

    return OpenAIChatCompletionClient(
        model=model,
        api_key=GROQ_API_KEY,
        base_url=BASE_URL,
        temperature=temperature,
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "structured_output": True,
            "family": "unknown",
        },
    )
