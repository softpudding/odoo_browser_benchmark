"""Pure JSON-RPC oracle for mrp.create_bom_with_components.

This oracle does NOT use a browser. It proves the task is solvable by
hitting Odoo's JSON-RPC endpoint directly:
  1. Find the seeded finished product 'Bench Assembled Gadget' and the
     three component products.
  2. Delete any stray mrp.bom on the finished product (defensive cleanup).
  3. Create a single mrp.bom with product_tmpl_id, product_qty=1,
     code='BOM-REFERENCE', and three bom_line_ids via one2many tuples.

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

PRODUCT_NAME = "Bench Assembled Gadget"
BOM_CODE = "BOM-REFERENCE"
COMPONENTS = [
    ("Bench Steel Frame", 1.0),
    ("Bench Control Board", 1.0),
    ("Bench Power Unit", 2.0),
]


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

    # -----------------------------------------------------------------
    # 1. Locate the seeded finished product template.
    # -----------------------------------------------------------------
    product_tmpl = execute_kw(
        BASE_URL, DB, uid, PASSWORD,
        "product.template", "search_read",
        [[("name", "=", PRODUCT_NAME)]],
        {"fields": ["id", "name"], "limit": 1},
    )
    if not product_tmpl:
        raise RuntimeError(f"product.template '{PRODUCT_NAME}' not found (seed may have failed)")
    product_tmpl_id = product_tmpl[0]["id"]

    # Resolve each component name to its product.product (variant).
    component_vals = []
    for comp_name, qty in COMPONENTS:
        prods = execute_kw(
            BASE_URL, DB, uid, PASSWORD,
            "product.product", "search_read",
            [[("name", "=", comp_name)]],
            {"fields": ["id", "name"], "limit": 1},
        )
        if not prods:
            raise RuntimeError(f"Component product '{comp_name}' not found (seed may have failed)")
        component_vals.append((prods[0]["id"], qty))

    # -----------------------------------------------------------------
    # 2. Defensive cleanup: remove any stray BoMs on this template.
    # -----------------------------------------------------------------
    existing_boms = execute_kw(
        BASE_URL, DB, uid, PASSWORD,
        "mrp.bom", "search",
        [[("product_tmpl_id", "=", product_tmpl_id)]],
        {},
    )
    if existing_boms:
        execute_kw(
            BASE_URL, DB, uid, PASSWORD,
            "mrp.bom", "unlink",
            [existing_boms],
        )

    # -----------------------------------------------------------------
    # 3. Create the mrp.bom with three bom_line_ids via one2many tuples.
    # -----------------------------------------------------------------
    bom_vals = {
        "product_tmpl_id": product_tmpl_id,
        "product_qty": 1.0,
        "code": BOM_CODE,
        "bom_line_ids": [
            (0, 0, {"product_id": prod_id, "product_qty": qty})
            for prod_id, qty in component_vals
        ],
    }
    bom_id = execute_kw(
        BASE_URL, DB, uid, PASSWORD,
        "mrp.bom", "create",
        [bom_vals],
    )
    print(f"Created mrp.bom id={bom_id} for product_tmpl_id={product_tmpl_id}")
    print("Oracle: PASS")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # noqa: BLE001
        print(f"Oracle: FAIL - {exc}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)
