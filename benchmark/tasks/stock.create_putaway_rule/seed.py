"""Seed for stock.create_putaway_rule.

Category: deep_ui_interaction (HARD).

Set up the prerequisites for the agent to create a putaway rule:
- A sub-location "Shelf A1" under WH/Stock (so the dest location exists).
- A storable product "Storage Box Echo" that the rule will target.
- A distractor storable product "Storage Box Foxtrot" — the agent must NOT
  create a rule for this one.

Cleans up any prior putaway rules for these products so re-runs start fresh.
"""

TARGET_PRODUCT = "Storage Box Echo"
DISTRACTOR_PRODUCT = "Storage Box Foxtrot"
SHELF_NAME = "Shelf A1"
STOCK_COMPLETE = "WH/Stock"


def _cleanup(env):
    prods = env["product.product"].search([
        ("name", "in", [TARGET_PRODUCT, DISTRACTOR_PRODUCT])
    ])
    if prods:
        env["stock.putaway.rule"].search([
            ("product_id", "in", prods.ids)
        ]).unlink()


def _ensure_stock_location(env):
    loc = env["stock.location"].search([
        ("complete_name", "=", STOCK_COMPLETE),
        ("usage", "=", "internal"),
    ], limit=1)
    if not loc:
        # Fall back to the main warehouse's lot_stock_id
        wh = env["stock.warehouse"].search([], limit=1)
        loc = wh.lot_stock_id
    return loc


def _ensure_shelf(env, parent_stock):
    shelf = env["stock.location"].search([
        ("name", "=", SHELF_NAME),
        ("location_id", "=", parent_stock.id),
    ], limit=1)
    if not shelf:
        shelf = env["stock.location"].create({
            "name": SHELF_NAME,
            "location_id": parent_stock.id,
            "usage": "internal",
        })
    return shelf


def _ensure_product(env, name):
    product = env["product.product"].search([("name", "=", name)], limit=1)
    if not product:
        tmpl = env["product.template"].create({
            "name": name,
            "type": "consu",
            "is_storable": True,
            "list_price": 15.0,
        })
        product = tmpl.product_variant_id
    else:
        product.product_tmpl_id.write({
            "type": "consu",
            "is_storable": True,
        })
    return product


def setup(env):
    _cleanup(env)

    stock_loc = _ensure_stock_location(env)
    _ensure_shelf(env, stock_loc)

    _ensure_product(env, TARGET_PRODUCT)
    _ensure_product(env, DISTRACTOR_PRODUCT)
