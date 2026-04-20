"""Shared environment setup for benchmark agent wrappers.

Configures OPENAI_API_KEY and OPENAI_BASE_URL from DashScope env vars
if OpenAI keys are not already set. This lets all agents that support
OpenAI-compatible APIs work with DashScope/Bailian.
"""

import os
import sys

# DashScope OpenAI-compatible endpoint
DASHSCOPE_OPENAI_BASE = "https://dashscope.aliyuncs.com/compatible-mode/v1"

# Default model for DashScope (vision-capable for browser agents)
DASHSCOPE_DEFAULT_MODEL = "qwen3.6-plus"


def setup_openai_compat():
    """Set OPENAI_API_KEY and OPENAI_BASE_URL from DashScope if needed.

    Priority:
    1. OPENAI_API_KEY already set -> use as-is
    2. DASHSCOPE_API_KEY set -> map to OpenAI-compatible endpoint
    3. BAILIAN_API_KEY set -> map to OpenAI-compatible endpoint
    """
    if os.environ.get("OPENAI_API_KEY"):
        return  # Already configured

    dashscope_key = os.environ.get("DASHSCOPE_API_KEY") or os.environ.get("BAILIAN_API_KEY")
    if dashscope_key:
        os.environ["OPENAI_API_KEY"] = dashscope_key
        os.environ.setdefault(
            "OPENAI_BASE_URL",
            os.environ.get("DASHSCOPE_BASE_URL")
            or os.environ.get("BAILIAN_BASE_URL")
            or DASHSCOPE_OPENAI_BASE,
        )
        return

    print(
        "ERROR: No LLM API key found. Set one of: "
        "OPENAI_API_KEY, DASHSCOPE_API_KEY, BAILIAN_API_KEY",
        file=sys.stderr,
    )
    sys.exit(1)


def get_env(name):
    """Get a required environment variable or exit."""
    val = os.environ.get(name, "")
    if not val:
        print(f"ERROR: {name} not set", file=sys.stderr)
        sys.exit(1)
    return val


def get_model():
    """Get the LLM model name, defaulting to DashScope's vision model."""
    return os.environ.get("BENCHMARK_MODEL") or DASHSCOPE_DEFAULT_MODEL


def build_instruction():
    """Build the full instruction with login context prepended."""
    instruction = get_env("BENCHMARK_INSTRUCTION")
    start_url = get_env("BENCHMARK_START_URL")
    login = os.environ.get("BENCHMARK_LOGIN", "")
    password = os.environ.get("BENCHMARK_PASSWORD", "")

    parts = [f"Go to {start_url}."]
    if login:
        parts.append(f"Log in with username '{login}' and password '{password}'.")
    parts.append(instruction)
    return " ".join(parts)
