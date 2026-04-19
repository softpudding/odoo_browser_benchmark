"""Seed for stock.create_physical_inventory_adjust_two_products (medium).

Category 5: Deep UI interaction (inline editable tree view).

Seeds:
  * Admin is granted ``stock.group_stock_multi_locations`` so that the
    virtual ``Inventory adjustment`` location is reachable and the
    Physical Inventory list surfaces the full location column (needed
    for the state-diff oracle to track mirror quants keyed by location).
  * Storable product ``Bench Prod X`` with 15 units on-hand at WH/Stock.
  * Storable product ``Bench Prod Y`` with 25 units on-hand at WH/Stock.

The agent must open Inventory > Operations > Physical Inventory, edit
the Counted Quantity cell inline (15 -> 12 for X, 25 -> 27 for Y), then
click Apply All (or per-row Apply) and confirm the Inventory Adjustment
Reference dialog. Odoo creates one ``stock.move`` with
``is_inventory=True, state='done'`` per adjusted product and writes
``stock.quant.quantity`` to match the counted value.
"""

PRODUCT_X = "Bench Prod X"
PRODUCT_Y = "Bench Prod Y"
QTY_X = 15.0
QTY_Y = 25.0


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
        [("name", "in", [PRODUCT_X, PRODUCT_Y])]
    )
    if products:
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

    # Grant admin the multi-locations group so the virtual
    # `Inventory adjustment` location is reachable and the Physical
    # Inventory list shows the full location path (needed for the
    # mirror-quant state-diff and for humans to disambiguate rows when
    # multiple locations exist).
    admin = env.ref("base.user_admin")
    admin.group_ids |= env.ref("stock.group_stock_multi_locations")

    location = _find_stock_location(env)
    if not location:
        raise ValueError(
            "Cannot find WH/Stock location - stock module not configured"
        )

    for name, qty in [(PRODUCT_X, QTY_X), (PRODUCT_Y, QTY_Y)]:
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
