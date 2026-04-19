"""Pure JSON-RPC oracle for website_sale.publish_product_shop.

This oracle does NOT use a browser. It proves the task is solvable by hitting
Odoo's JSON-RPC endpoint directly:
  1. Locate the seeded "Bench Gadget Pro" product.template.
  2. Write list_price=99.0 and is_published=True on it.

Environment variables (set by eval.py --agent oracle):
  BENCHMARK_BASE_URL   -- e.g. http://127.0.0.1:8069
  BENCHMARK_DB         -- target database
  BENCHMARK_LOGIN      -- login (default "admin")
  BENCHMARK_PASSWORD   -- password (default "admin")
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request

BASE_URL = os.environ.get("BENCHMARK_BASE_URL", "http://127.0.0.1:8069").rstrip("/")
DB = os.environ.get("BENCHMARK_DB", "")
LOGIN = os.environ.get("BENCHMARK_LOGIN") or "admin"
PASSWORD = os.environ.get("BENCHMARK_PASSWORD") or "admin"

PRODUCT_NAME = "Bench Gadget Pro"
TARGET_PRICE = 99.0


def jsonrpc_call(url: str, service: str, method: str, args: list):
    """Low-level JSON-RPC call to Odoo."""
    payload = {
        "jsonrpc": "2.0",
        "method": "call",
        "params": {
            "service": service,
            "method": method,
            "args": args,
        },
        "id": 1,
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{url}/jsonrpc",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        body = json.loads(resp.read().decode("utf-8"))
    if "error" in body:
        raise RuntimeError(f"JSON-RPC error: {body['error']}")
    return body.get("result")


def authenticate(base_url: str, db: str, login: str, password: str) -> int:
    uid = jsonrpc_call(base_url, "common", "authenticate", [db, login, password, {}])
    if not uid:
        raise RuntimeError(f"JSON-RPC auth failed for {login}@{db}")
    return uid


def execute_kw(base_url, db, uid, password, model, method, args, kwargs=None):
    return jsonrpc_call(
        base_url, "object", "execute_kw",
        [db, uid, password, model, method, args, kwargs or {}],
    )


def main():
    if not DB:
        print("ERROR: BENCHMARK_DB is not set", file=sys.stderr)
        sys.exit(1)

    uid = authenticate(BASE_URL, DB, LOGIN, PASSWORD)

    products = execute_kw(
        BASE_URL, DB, uid, PASSWORD,
        "product.template", "search_read",
        [[("name", "=", PRODUCT_NAME)]],
        {"fields": ["id", "name", "list_price", "is_published"], "limit": 1},
    )
    if not products:
        raise RuntimeError(
            f"product.template '{PRODUCT_NAME}' not found (seed may have failed)"
        )
    product_id = products[0]["id"]

    execute_kw(
        BASE_URL, DB, uid, PASSWORD,
        "product.template", "write",
        [[product_id], {
            "list_price": TARGET_PRICE,
            "is_published": True,
        }],
    )
    print(f"Updated product.template id={product_id}: list_price={TARGET_PRICE}, is_published=True")
    print("Oracle: PASS")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"Oracle: FAIL - {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
