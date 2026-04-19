"""Seed for stock.adjust_inventory_count_apply_moves (medium).

Category 5: Deep UI interaction (inline editable tree view).

Seeds:
  * Storable product 'Bench Prod A' with 20 units on-hand at WH/Stock.
  * Storable product 'Bench Prod B' with 15 units on-hand at WH/Stock.

The agent must open Inventory > Operations > Physical Inventory, edit
the Counted Quantity cell inline (20 -> 18 for A, 15 -> 16 for B), then
click Apply All (or per-row Apply). Odoo creates one stock.move with
is_inventory=True per adjusted product and updates stock.quant.quantity.
"""

PRODUCT_A = "Bench Prod A"
PRODUCT_B = "Bench Prod B"
QTY_A = 20.0
QTY_B = 15.0


def _find_stock_location(env):
    location = env["stock.location"].search(
        [("complete_name", "=", "WH/Stock")], limit=1
    )
    if not location:
        location = env["stock.location"].search(
            [("name", "=", "Stock"), ("usage", "=", "internal")], limit=1
        )
    return location


def _cleanup(env):
    products = env["product.product"].search(
        [("name", "in", [PRODUCT_A, PRODUCT_B])]
    )
    if products:
        # Remove moves (including is_inventory adjustments) and move lines
        try:
            env["stock.move.line"].search(
                [("product_id", "in", products.ids)]
            ).sudo().unlink()
        except Exception:
            pass
        try:
            env["stock.move"].search(
                [("product_id", "in", products.ids)]
            ).sudo().unlink()
        except Exception:
            pass
        # Remove quants
        try:
            env["stock.quant"].with_context(inventory_mode=True).search(
                [("product_id", "in", products.ids)]
            ).sudo().unlink()
        except Exception:
            pass
        try:
            products.mapped("product_tmpl_id").sudo().unlink()
        except Exception:
            pass


def setup(env):
    _cleanup(env)

    location = _find_stock_location(env)
    if not location:
        raise ValueError(
            "Cannot find WH/Stock location — stock module not configured"
        )

    for name, qty in [(PRODUCT_A, QTY_A), (PRODUCT_B, QTY_B)]:
        product = env["product.product"].search(
            [("name", "=", name)], limit=1
        )
        if not product:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "consu",
                "is_storable": True,
                "tracking": "none",
                "list_price": 10.0,
                "standard_price": 5.0,
                "sale_ok": True,
                "purchase_ok": True,
            })
            product = tmpl.product_variant_id
        env["stock.quant"]._update_available_quantity(
            product, location, qty
        )

    # Force flush
    env.cr.execute("SELECT 1")
