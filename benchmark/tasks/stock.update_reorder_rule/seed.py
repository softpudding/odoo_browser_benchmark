"""Seed reorder rules for the update_reorder_rule task.

Category 2 (MEDIUM): Navigate to inventory reorder rules and update the min/max
quantities for a specific product. The agent must find the right inline row in
the reorder rules list and change two numeric fields.
"""

TARGET_PRODUCT = "Steel Bracket 12\""
DISTRACTOR_PRODUCT = "Copper Wire 100m"

TARGET_MIN_QTY = 10.0
TARGET_MAX_QTY = 50.0
DISTRACTOR_MIN_QTY = 20.0
DISTRACTOR_MAX_QTY = 100.0


def _cleanup(env):
    products = env["product.product"].search([
        ("name", "in", [TARGET_PRODUCT, DISTRACTOR_PRODUCT])
    ])
    if products:
        env["stock.warehouse.orderpoint"].search([
            ("product_id", "in", products.ids)
        ]).unlink()


def _ensure_product(env, name):
    product = env["product.product"].search([("name", "=", name)], limit=1)
    if not product:
        tmpl = env["product.template"].create({
            "name": name,
            "type": "consu",
        })
        product = tmpl.product_variant_id
    return product


def _ensure_orderpoint(env, product, location, min_qty, max_qty):
    orderpoint = env["stock.warehouse.orderpoint"].search([
        ("product_id", "=", product.id),
        ("location_id", "=", location.id),
    ], limit=1)
    if orderpoint:
        orderpoint.write({
            "product_min_qty": min_qty,
            "product_max_qty": max_qty,
        })
    else:
        env["stock.warehouse.orderpoint"].create({
            "product_id": product.id,
            "location_id": location.id,
            "product_min_qty": min_qty,
            "product_max_qty": max_qty,
        })


def setup(env):
    _cleanup(env)

    location = env["stock.location"].search([
        ("complete_name", "ilike", "WH/Stock"),
        ("usage", "=", "internal"),
    ], limit=1)
    if not location:
        location = env["stock.warehouse"].search([], limit=1).lot_stock_id

    target = _ensure_product(env, TARGET_PRODUCT)
    distractor = _ensure_product(env, DISTRACTOR_PRODUCT)

    _ensure_orderpoint(env, target, location, TARGET_MIN_QTY, TARGET_MAX_QTY)
    _ensure_orderpoint(env, distractor, location, DISTRACTOR_MIN_QTY, DISTRACTOR_MAX_QTY)
