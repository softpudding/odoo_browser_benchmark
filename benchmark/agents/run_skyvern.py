#!/usr/bin/env python3
"""Benchmark wrapper for Skyvern (https://github.com/skyvern-ai/skyvern).

Setup:
    pip install skyvern

Usage:
    uv run benchmark-eval run <task> --agent command \
        --cmd "python benchmark/agents/skyvern_agent.py"
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _env_setup import setup_openai_compat, get_env, get_model, build_instruction

setup_openai_compat()


async def main():
    from skyvern import Skyvern
    from skyvern.forge.sdk.api.llm.models import LLMConfig, LiteLLMParams

    start_url = get_env("BENCHMARK_START_URL")
    full_instruction = build_instruction()
    max_steps = int(os.environ.get("BENCHMARK_MAX_STEPS", "200"))
    model = get_model()

    # Skyvern uses LiteLLM — configure via LLMConfig + env vars
    # OPENAI_API_KEY and OPENAI_BASE_URL are already set by _env_setup
    llm_config = LLMConfig(
        model_name=f"openai/{model}",
        required_env_vars=["OPENAI_API_KEY"],
        supports_vision=True,
        add_assistant_prefix=False,
        litellm_params=LiteLLMParams(
            api_base=os.environ.get("OPENAI_BASE_URL"),
        ),
    )

    skyvern = Skyvern.local(
        llm_config=llm_config,
        settings={
            "BLOCKED_HOSTS": [],
            "ALLOWED_HOSTS": ["127.0.0.1", "localhost"],
        },
    )

    result = await skyvern.run_task(
        url=start_url,
        prompt=full_instruction,
        max_steps=max_steps,
    )

    print(f"Skyvern result: {result}")
    status = getattr(result, "status", None)
    if status and "completed" in str(status).lower():
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
