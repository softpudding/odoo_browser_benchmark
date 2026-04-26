#!/usr/bin/env python3
"""Benchmark wrapper for Alumnium (https://github.com/alumnium-hq/alumnium).

Setup:
    pip install alumnium langchain-openai

Note: Alumnium is step-level NL (do/check/get), not a full autonomous agent.
This wrapper passes the entire task as a single do() call.

Usage:
    uv run benchmark-eval run <task> --agent command \
        --cmd "python benchmark/agents/run_alumnium.py"
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _env_setup import setup_openai_compat, get_env, build_instruction, get_model

setup_openai_compat()


def main():
    from langchain_openai import ChatOpenAI
    from playwright.sync_api import sync_playwright
    from alumnium import Alumni

    start_url = get_env("BENCHMARK_START_URL")
    full_instruction = build_instruction()
    model = get_model()

    # DashScope doesn't support json_object response_format without "json" in
    # the prompt. Force all with_structured_output calls to use function_calling.
    orig_wso = ChatOpenAI.with_structured_output

    def patched_wso(self, schema=None, *, method="function_calling", **kwargs):
        return orig_wso(self, schema, method=method, **kwargs)

    ChatOpenAI.with_structured_output = patched_wso

    llm = ChatOpenAI(
        model=model,
        api_key=os.environ.get("OPENAI_API_KEY", ""),
        base_url=os.environ.get("OPENAI_BASE_URL"),
        temperature=0.0,
        model_kwargs={
            "extra_body": {"enable_thinking": False},
        },
    )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.set_default_navigation_timeout(120_000)
        page.goto(start_url, wait_until="domcontentloaded")

        al = Alumni(page, llm=llm)

        try:
            al.do(full_instruction)
            print("Alumnium: task executed")
            sys.exit(0)
        except Exception as e:
            print(f"Alumnium error: {e}", file=sys.stderr)
            sys.exit(1)
        finally:
            browser.close()


if __name__ == "__main__":
    main()
