#!/usr/bin/env python3
"""Benchmark wrapper for Notte (https://github.com/nottelabs/notte).

Setup:
    pip install notte

Usage:
    uv run benchmark-eval run <task> --agent command \
        --cmd "python benchmark/agents/run_notte.py"
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _env_setup import setup_openai_compat, get_env, build_instruction, get_model

setup_openai_compat()

# Notte uses litellm — configure OpenAI-compatible base URL
os.environ.setdefault("OPENAI_API_BASE", os.environ.get("OPENAI_BASE_URL", ""))


def main():
    from notte import Agent, Session

    full_instruction = build_instruction()
    start_url = get_env("BENCHMARK_START_URL")
    model = get_model()
    max_steps = int(os.environ.get("BENCHMARK_MAX_STEPS", "200"))

    # Use litellm format: openai/<model_name>
    litellm_model = f"openai/{model}"

    with Session(headless=False) as session:
        agent = Agent(session, reasoning_model=litellm_model, max_steps=max_steps)
        result = agent.run(task=full_instruction, url=start_url)

        print(f"Notte result: {result}")
        if result and getattr(result, "success", False):
            sys.exit(0)
        else:
            sys.exit(1)


if __name__ == "__main__":
    main()
