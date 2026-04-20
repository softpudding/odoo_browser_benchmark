#!/usr/bin/env python3
"""Benchmark wrapper for WebSight (https://github.com/SuperAce100/websight).

Setup:
    pip install websight

Usage:
    uv run benchmark-eval run <task> --agent command \
        --cmd "python benchmark/agents/run_websight.py"
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from _env_setup import setup_openai_compat, build_instruction, get_model

setup_openai_compat()

# WebSight hardcodes OpenRouter — override before import
os.environ.setdefault("OPENROUTER_API_KEY", os.environ.get("OPENAI_API_KEY", ""))


def main():
    from openai import OpenAI

    model = get_model()
    api_key = os.environ.get("OPENAI_API_KEY", "")
    base_url = os.environ.get("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")

    # Patch the OpenAI client at the llm module level
    import websight.model.llm as llm_mod
    llm_mod.client = OpenAI(api_key=api_key, base_url=base_url)
    llm_mod.text_model = model

    # Patch hardcoded model constants in agent.py
    import websight.agent.agent as agent_mod
    agent_mod.PLANNING_MODEL = model
    agent_mod.NEXT_ACTION_MODEL = model

    # Fix upstream bug: execute_action passes (action, history, screenshot)
    # but websight_call expects (prompt, image_base64, history). Swap args.
    import websight.model.websight as ws_mod
    orig_websight_call = ws_mod.websight_call

    def fixed_execute_action(self, next_action, history):
        current_state = self.browser.get_state()
        import re
        url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+'
        url_match = re.search(url_pattern, next_action)
        if url_match:
            url = url_match.group(0)
            self.browser.goto_url(url)
            from websight.model.websight import Action
            return Action(action="goto_url", args={"url": url}, reasoning=f"Navigated to {url}")

        # Use llm_call_image instead of websight_call (which uses a local model)
        # since we're routing through an API-based VLM
        screenshot = current_state.page_screenshot_base64
        prompt = f"You are a browser automation agent. Given the screenshot and task, output an action.\nTask: {next_action}\nHistory: {history}\nRespond with a JSON object: {{\"action\": \"<action_type>\", \"args\": {{...}}, \"reasoning\": \"<why>\"}}\nActions: click(element_id), type(element_id, text), scroll(direction), goto_url(url), finished()"
        response = llm_mod.llm_call_image(screenshot, prompt, model=model)
        try:
            import json
            data = json.loads(response)
            from websight.model.websight import Action
            return Action(**data)
        except Exception:
            from websight.model.websight import Action
            return Action(action="finished", args={}, reasoning=response)

    agent_mod.Agent.execute_action = fixed_execute_action

    from websight import Agent

    full_instruction = build_instruction()
    max_steps = int(os.environ.get("BENCHMARK_MAX_STEPS", "200"))

    agent = Agent(show_browser=True)
    result = agent.run(task=full_instruction, max_iterations=max_steps)

    print(f"WebSight result: {result}")
    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
