"""Seed for stock.create_scrap_order_for_damaged_qty.

Category: deep_ui_interaction (MEDIUM). The agent must open the Scrap
Orders list via Inventory > Operations > Scrap, click New, pick product
'Bench Scrap Item', OVERRIDE the default scrap_qty (1.0 -> 3.0), save,
then click Validate on the form header to push the scrap to state 'done'.

Seeds:
  * Storable product 'Bench Scrap Item' with 10 units on-hand at
    WH/Stock via env["stock.quant"]._update_available_quantity. The
    product is type='consu' + is_storable=True (Odoo 19 replacement for
    the legacy type='product') so scrap can properly debit inventory.
  * Admin is granted `stock.group_stock_multi_locations` so the source
    /scrap location fields are visible and editable on the wizard — we
    only use the default WH/Stock and default Virtual Locations/Scrap,
    but without the group the fields silently default-bind and the
    oracle cannot assert on them.

Failure modes the seed is designed to expose:
  * Agent creates the scrap from the product's on-form Scrap button
    instead of Operations > Scrap > New (check.py does not require the
    entry-point, but the default prefill on that wizard differs).
  * Agent leaves scrap_qty at the default 1.0.
  * Agent saves the scrap but forgets to click Validate, leaving
    state='draft'.
"""

PRODUCT_NAME = "Bench Scrap Item"
ON_HAND_QTY = 10.0


def _cleanup(env):
    # Remove any prior scrap orders for the product (draft ones are
    # unlinkable; done ones are intentionally preserved because they
    # would have created on-hand movements, but the _update_available_
    # quantity call below will reset to exactly 10 regardless).
    prods = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if prods:
        try:
            env["stock.scrap"].with_context(active_test=False).search([
                ("product_id", "in", prods.ids),
                ("state", "=", "draft"),
            ]).unlink()
        except Exception:
            pass
        # Clear stray move lines / moves that are NOT linked to a done
        # scrap (done scraps own immutable stock moves that we must not
        # touch, but unrelated residue from prior runs can be removed).
        try:
            env["stock.move.line"].search([
                ("product_id", "in", prods.ids),
                ("state", "not in", ("done", "cancel")),
            ]).unlink()
        except Exception:
            pass
        try:
            env["stock.move"].search([
                ("product_id", "in", prods.ids),
                ("state", "not in", ("done", "cancel")),
            ]).unlink()
        except Exception:
            pass
        # Drop on-hand quants on the product so we can reseed from
        # zero. Done moves live on forever; that is fine.
        try:
            env["stock.quant"].with_context(inventory_mode=True).search([
                ("product_id", "in", prods.ids),
            ]).unlink()
        except Exception:
            pass
        try:
            prods.mapped("product_tmpl_id").unlink()
        except Exception:
            pass


def setup(env):
    _cleanup(env)

    # Grant admin the multi-locations group so the scrap form surfaces
    # the Source Location + Scrap Location fields (gated by
    # stock.group_stock_multi_locations).
    admin = env.ref("base.user_admin")
    admin.group_ids |= env.ref("stock.group_stock_multi_locations")

    # Storable product.
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
        "list_price": 15.0,
        "standard_price": 10.0,
        "sale_ok": False,
        "purchase_ok": False,
    })
    product = tmpl.product_variant_id

    # Seed 10 units on-hand at WH/Stock.
    wh = env["stock.warehouse"].search(
        [("company_id", "=", env.company.id)], limit=1
    )
    if not wh:
        wh = env["stock.warehouse"].search([], limit=1)
    stock_location = wh.lot_stock_id

    env["stock.quant"]._update_available_quantity(
        product, stock_location, ON_HAND_QTY
    )
