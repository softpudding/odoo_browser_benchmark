#!/usr/bin/env python3

import argparse
import asyncio
import json
import os
import random
import sys
import tempfile
from pathlib import Path
from urllib.parse import urljoin, urlparse
from xmlrpc import client as xmlrpclib


def env_int(name, default):
    value = os.getenv(name)
    if not value:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def build_parser():
    parser = argparse.ArgumentParser(
        description="Run Browser Use against a local Odoo instance with a local browser.",
    )
    parser.add_argument(
        "task",
        nargs="?",
        help="Natural-language task for the browser agent.",
    )
    parser.add_argument(
        "--base-url",
        default=os.getenv("ODOO_BROWSER_USE_BASE_URL", "http://127.0.0.1:8069"),
        help="Base URL for the local Odoo instance.",
    )
    parser.add_argument(
        "--start-path",
        default="/odoo",
        help="Initial path the agent should open on the Odoo instance.",
    )
    parser.add_argument(
        "--login",
        help="Login to use if the Odoo instance prompts for authentication.",
    )
    parser.add_argument(
        "--password",
        help="Password to use with --login.",
    )
    parser.add_argument(
        "--db",
        help="Database name to pick if the login screen asks for one.",
    )
    parser.add_argument(
        "--browser",
        choices=("chromium", "real"),
        default=os.getenv("ODOO_BROWSER_USE_BROWSER", "chromium"),
        help="Local browser mode.",
    )
    parser.add_argument(
        "--profile",
        help="Chrome profile directory name when using --browser real.",
    )
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Show the browser window while the agent runs.",
    )
    parser.add_argument(
        "--provider",
        choices=("auto", "browser-use", "openai-compatible", "dashscope"),
        default=os.getenv("ODOO_BROWSER_USE_PROVIDER", "auto"),
        help="Model provider used by browser-use.",
    )
    parser.add_argument(
        "--model",
        default=os.getenv("ODOO_BROWSER_USE_MODEL"),
        help="Model name for the selected provider.",
    )
    parser.add_argument(
        "--llm-base-url",
        default=os.getenv("OPENAI_COMPATIBLE_BASE_URL"),
        help="Base URL for OpenAI-compatible providers.",
    )
    parser.add_argument(
        "--api-key-var",
        help="Environment variable name containing the model API key.",
    )
    parser.add_argument(
        "--max-steps",
        type=int,
        default=40,
        help="Maximum number of agent steps.",
    )
    parser.add_argument(
        "--llm-timeout",
        type=int,
        default=env_int("ODOO_BROWSER_USE_LLM_TIMEOUT", 180),
        help="Seconds to wait for each LLM call before retrying.",
    )
    parser.add_argument(
        "--step-timeout",
        type=int,
        default=env_int("ODOO_BROWSER_USE_STEP_TIMEOUT", 240),
        help="Seconds to wait for each browser step.",
    )
    parser.add_argument(
        "--list-profiles",
        action="store_true",
        help="List local Chrome profiles visible to browser-use.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the resolved configuration without running the agent.",
    )
    parser.add_argument(
        "--eval-spec-file",
        help="Path to an agent-eval JSON spec file. When set, start and finalize an eval session around the run.",
    )
    parser.add_argument(
        "--eval-case",
        help="Built-in agent-eval case name to prepare on the server before the run.",
    )
    parser.add_argument(
        "--list-eval-cases",
        action="store_true",
        help="List built-in agent-eval case names available on the server.",
    )
    parser.add_argument(
        "--eval-name",
        help="Optional display name stored in the eval session metadata.",
    )
    return parser


def import_browser_use():
    try:
        from browser_use import Agent, Browser, ChatBrowserUse, ChatOpenAI
    except ImportError as exc:
        raise SystemExit(
            "browser_use Python package is not available in this interpreter. "
            "Use the Python where browser-use is installed, then retry.",
        ) from exc
    return Agent, Browser, ChatBrowserUse, ChatOpenAI


def build_task(args):
    start_url = urljoin(f"{args.base_url.rstrip('/')}/", args.start_path.lstrip("/"))
    instructions = [
        f"You are testing a local Odoo instance at {args.base_url}.",
        f"Start by opening {start_url}.",
        "Stay focused on this Odoo instance unless the task explicitly requires another site.",
        "Do not use a remote or cloud browser for this task.",
    ]
    if args.db:
        instructions.append(f"If the database selector appears, choose {args.db}.")
    if args.login:
        instructions.append(f"If login is required, use login {args.login}.")
    if args.password:
        instructions.append(f"Use password {args.password}.")
    instructions.append(f"Task: {args.task}")
    return "\n".join(f"- {line}" for line in instructions)


def contains_non_ascii(text):
    return any(ord(char) > 127 for char in text)


def first_env(*names):
    for name in names:
        value = os.getenv(name)
        if value:
            return name, value
    return None, None


def pick_browser_use_api_key():
    pool_names = []
    explicit_pool = os.getenv("BROWSER_USE_API_KEY_POOL", "")
    if explicit_pool:
        pool_names.extend(name for name in explicit_pool.split() if name)

    if not pool_names:
        pool_names.extend(
            sorted(
                name
                for name in os.environ
                if name.startswith("BROWSER_USE_API_KEY_")
            )
        )

    candidates = []
    for name in pool_names:
        value = os.getenv(name)
        if value:
            candidates.append((name, value))

    if candidates:
        return random.SystemRandom().choice(candidates)

    return "BROWSER_USE_API_KEY", os.getenv("BROWSER_USE_API_KEY")


def resolve_provider(args):
    provider = args.provider
    model = args.model or ""

    if provider == "auto":
        if os.getenv("DASHSCOPE_API_KEY") or os.getenv("BAILIAN_API_KEY") or model.startswith("glm"):
            return "dashscope"
        if args.llm_base_url or os.getenv("OPENAI_API_KEY"):
            return "openai-compatible"
        return "browser-use"
    return provider


def resolve_llm_config(args):
    provider = resolve_provider(args)

    if provider == "browser-use":
        if args.api_key_var:
            api_key_var = args.api_key_var
            api_key = os.getenv(api_key_var)
        else:
            api_key_var, api_key = pick_browser_use_api_key()
        return {
            "provider": provider,
            "model": args.model or "bu-latest",
            "base_url": None,
            "api_key_var": api_key_var,
            "api_key": api_key,
        }

    if provider == "dashscope":
        if args.api_key_var:
            api_key_var = args.api_key_var
            api_key = os.getenv(api_key_var)
        else:
            api_key_var, api_key = first_env("DASHSCOPE_API_KEY", "BAILIAN_API_KEY", "OPENAI_API_KEY")
            api_key_var = api_key_var or "DASHSCOPE_API_KEY"
        return {
            "provider": provider,
            "model": args.model or "qwen-vl-max",
            "base_url": (
                args.llm_base_url
                or os.getenv("DASHSCOPE_BASE_URL")
                or os.getenv("BAILIAN_BASE_URL")
                or "https://dashscope.aliyuncs.com/compatible-mode/v1"
            ),
            "api_key_var": api_key_var,
            "api_key": api_key,
        }

    api_key_var = args.api_key_var or "OPENAI_API_KEY"
    return {
        "provider": provider,
        "model": args.model or "gpt-5-mini",
        "base_url": args.llm_base_url or os.getenv("OPENAI_BASE_URL"),
        "api_key_var": api_key_var,
        "api_key": os.getenv(api_key_var),
    }


def build_llm(llm_config, ChatBrowserUse, ChatOpenAI):
    api_key = llm_config["api_key"]
    api_key_var = llm_config["api_key_var"]
    provider = llm_config["provider"]

    if not api_key:
        if provider == "dashscope":
            raise SystemExit(
                "DashScope / Bailian key not found. Set one of "
                "`DASHSCOPE_API_KEY`, `BAILIAN_API_KEY`, or pass `--api-key-var YOUR_ENV_VAR`.",
            )
        raise SystemExit(
            f"Environment variable {api_key_var!r} is not set, so provider {provider!r} cannot run.",
        )

    if provider == "browser-use":
        return ChatBrowserUse(model=llm_config["model"], api_key=api_key)

    return ChatOpenAI(
        model=llm_config["model"],
        api_key=api_key,
        base_url=llm_config["base_url"],
        temperature=0.0,
        add_schema_to_system_prompt=True,
        dont_force_structured_output=True,
        remove_min_items_from_schema=True,
        remove_defaults_from_schema=True,
    )


def build_browser(args, Browser):
    parsed_base_url = urlparse(args.base_url)
    allowed_domains = [parsed_base_url.hostname] if parsed_base_url.hostname else None
    system_chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

    if args.profile and args.browser != "real":
        raise SystemExit("--profile only works with --browser real.")

    if args.browser == "real":
        browser_kwargs = {
            "headless": not args.headed,
            "allowed_domains": allowed_domains,
            "enable_default_extensions": False,
        }
        try:
            if args.profile:
                return Browser.from_system_chrome(profile_directory=args.profile, **browser_kwargs)
            return Browser.from_system_chrome(**browser_kwargs)
        except PermissionError as exc:
            raise SystemExit(
                "macOS blocked access to your Chrome profile directory. "
                "Use `--browser chromium` for this task, or grant Full Disk Access to the app "
                "running this command and retry `--browser real`."
            ) from exc

    browser_kwargs = {
        "use_cloud": False,
        "headless": not args.headed,
        "allowed_domains": allowed_domains,
        "enable_default_extensions": False,
        "user_data_dir": tempfile.mkdtemp(prefix="browser-use-odoo-"),
    }
    if system_chrome.exists():
        browser_kwargs["executable_path"] = str(system_chrome)

    return Browser(**browser_kwargs)


def require_eval_credentials(args):
    missing = []
    if not args.db:
        missing.append("--db")
    if not args.login:
        missing.append("--login")
    if not args.password:
        missing.append("--password")
    if missing:
        joined = ", ".join(missing)
        raise SystemExit(f"Evaluation mode requires {joined}.")


def xmlrpc_endpoints(base_url):
    base = argsafe_base_url(base_url)
    return (
        xmlrpclib.ServerProxy(f"{base}/xmlrpc/2/common"),
        xmlrpclib.ServerProxy(f"{base}/xmlrpc/2/object", use_datetime=True),
    )


def argsafe_base_url(base_url):
    return base_url.rstrip("/")


def load_eval_spec(path):
    try:
        with open(path, encoding="utf-8") as handle:
            return json.load(handle)
    except OSError as exc:
        raise SystemExit(f"Could not read eval spec file {path!r}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in eval spec file {path!r}: {exc}") from exc


def xmlrpc_login(args):
    require_eval_credentials(args)
    common_proxy, object_proxy = xmlrpc_endpoints(args.base_url)
    uid = common_proxy.authenticate(args.db, args.login, args.password, {})
    if not uid:
        raise SystemExit("Could not authenticate over XML-RPC.")
    return uid, object_proxy


def list_eval_cases(args):
    uid, object_proxy = xmlrpc_login(args)
    cases = object_proxy.execute_kw(
        args.db,
        uid,
        args.password,
        "agent.eval.case",
        "rpc_list_cases",
        [],
        {},
    )
    for case in cases:
        print(f"{case['name']}: {case['description']}")


def prepare_eval_case(args):
    uid, object_proxy = xmlrpc_login(args)
    return object_proxy.execute_kw(
        args.db,
        uid,
        args.password,
        "agent.eval.case",
        "rpc_prepare_case",
        [args.eval_case],
        {},
    )


def start_eval_session(args, spec, case_meta=None):
    uid, object_proxy = xmlrpc_login(args)
    meta = {
        "task": args.task,
        "provider": args.provider,
        "model": args.model,
        "browser": args.browser,
        "start_path": args.start_path,
        "base_url": args.base_url,
        "eval_case": args.eval_case,
    }
    if case_meta:
        meta["case_meta"] = case_meta
    if args.eval_name:
        meta["name"] = args.eval_name
    session = object_proxy.execute_kw(
        args.db,
        uid,
        args.password,
        "agent.eval.session",
        "rpc_start_session",
        [spec, meta],
        {},
    )
    return {
        "uid": uid,
        "object_proxy": object_proxy,
        "session": session,
    }


def finalize_eval_session(args, eval_context, *, state, final_result=None, last_url=None, errors=None):
    if not eval_context:
        return None
    meta = {
        "final_result": final_result,
        "last_url": last_url,
        "errors": errors or [],
    }
    return eval_context["object_proxy"].execute_kw(
        args.db,
        eval_context["uid"],
        args.password,
        "agent.eval.session",
        "rpc_finalize_session",
        [eval_context["session"]["id"], state, meta, "\n".join(errors or []) or None],
        {},
    )


async def translate_task_to_english(task, llm_config):
    from openai import AsyncOpenAI

    client = AsyncOpenAI(
        api_key=llm_config["api_key"],
        base_url=llm_config["base_url"],
    )
    response = await client.chat.completions.create(
        model=llm_config["model"],
        temperature=0.0,
        messages=[
            {
                "role": "system",
                "content": (
                    "Translate the user's browser automation task into clear English for an autonomous browser agent. "
                    "Preserve all URLs, names, numbers, quantities, dates, stage names, discounts, and expected outputs. "
                    "Do not summarize. Do not add commentary. Return only the translated task."
                ),
            },
            {
                "role": "user",
                "content": task,
            },
        ],
    )
    return (response.choices[0].message.content or "").strip()


def print_profiles(Browser):
    profiles = Browser.list_chrome_profiles()
    if not profiles:
        print("No Chrome profiles found")
        return

    for profile in profiles:
        label = profile.get("name") or profile.get("profile_directory") or str(profile)
        print(label)


async def run_agent(args):
    if args.list_eval_cases:
        list_eval_cases(args)
        return

    Agent, Browser, ChatBrowserUse, ChatOpenAI = import_browser_use()

    if args.list_profiles:
        print_profiles(Browser)
        return

    if args.eval_case and args.eval_spec_file:
        raise SystemExit("Use either --eval-case or --eval-spec-file, not both.")

    prepared_case = None

    if not args.task and not args.eval_case:
        raise SystemExit("Provide a task, or use --list-profiles.")

    llm_config = resolve_llm_config(args)
    if not args.task and args.eval_case and args.dry_run:
        args.task = f"Built-in eval case {args.eval_case!r} will provide the task at runtime."
    task = build_task(args)
    eval_context = None

    if llm_config["provider"] in {"dashscope", "openai-compatible"} and contains_non_ascii(task):
        translated_task = await translate_task_to_english(task, llm_config)
        if translated_task:
            print("Info: translated the task to English for agent compatibility.", file=sys.stderr)
            task = translated_task

    if args.dry_run:
        print(f"provider={llm_config['provider']}")
        print(f"model={llm_config['model']}")
        print(f"api_key_var={llm_config['api_key_var']}")
        print(f"api_key_present={bool(llm_config['api_key'])}")
        if llm_config["base_url"]:
            print(f"llm_base_url={llm_config['base_url']}")
        print(f"browser={args.browser}")
        print(f"profile={args.profile or ''}")
        print(f"headed={args.headed}")
        print(f"max_steps={args.max_steps}")
        print(f"llm_timeout={args.llm_timeout}")
        print(f"step_timeout={args.step_timeout}")
        print(f"eval_spec_file={args.eval_spec_file or ''}")
        print(f"eval_case={args.eval_case or ''}")
        print("\nTask:\n")
        print(task)
        return

    prepared_case = prepare_eval_case(args) if args.eval_case else None
    if not args.task and prepared_case:
        args.task = prepared_case["task"]
        task = build_task(args)

    eval_spec = load_eval_spec(args.eval_spec_file) if args.eval_spec_file else (prepared_case["spec"] if prepared_case else None)
    eval_context = start_eval_session(args, eval_spec, prepared_case.get("meta") if prepared_case else None) if eval_spec else None
    llm = build_llm(llm_config, ChatBrowserUse, ChatOpenAI)
    browser = build_browser(args, Browser)
    allowed_host = urlparse(args.base_url).hostname or args.base_url
    start_url = urljoin(f"{args.base_url.rstrip('/')}/", args.start_path.lstrip("/"))
    guardrails = (
        "Treat this as a brand-new task. Ignore any example tasks, memories, or hidden examples that mention "
        "Amazon, arXiv, LinkedIn, or any site that is not the current local Odoo instance. "
        f"Only browse pages on {allowed_host}. "
        f"If the current page is {start_url} or another page on {allowed_host}, describe only that page. "
        "If any remembered plan conflicts with the current URL or visible content, trust the current URL and page content instead. "
        "Do not invent search results, product lists, or external websites."
    )

    history = None
    eval_report = None
    run_error = None
    try:
        agent = Agent(
            task=task,
            llm=llm,
            browser=browser,
            llm_timeout=args.llm_timeout,
            step_timeout=args.step_timeout,
            extend_system_message=guardrails,
        )
        history = await agent.run(max_steps=args.max_steps)
    except Exception as exc:
        run_error = exc
    finally:
        await browser.stop()

    final_result = history.final_result() if history else None
    errors = [error for error in (history.errors() if history else []) if error]
    if run_error:
        errors.append(str(run_error))
    urls = [url for url in (history.urls() if history else []) if url]
    last_url = urls[-1] if urls else None
    session_state = "failed" if (run_error or errors) else "done"
    eval_report = finalize_eval_session(
        args,
        eval_context,
        state=session_state,
        final_result=final_result,
        last_url=last_url,
        errors=errors,
    )
    if run_error:
        raise run_error

    if final_result:
        print(final_result)
    else:
        print("Agent finished without a final result.")

    if errors:
        print("\nErrors:")
        for error in errors:
            print(f"- {error}")

    if last_url:
        print(f"\nLast URL: {last_url}")
    if eval_report:
        print("\nEvaluation:")
        print(json.dumps(eval_report, indent=2, sort_keys=True))


def main():
    args = build_parser().parse_args()
    asyncio.run(run_agent(args))


if __name__ == "__main__":
    main()
