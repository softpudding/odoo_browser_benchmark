"""Seed for stock.adjust_product_reorder_rule_min_max (medium).

Category 5: Deep UI interaction (smart-button gate + editable-list inline row).

Seeds:
  * Storable product 'Bench Reorder Item' (type='consu' + is_storable=True)
    at on-hand 0 at WH/Stock with NO pre-existing reordering rule. The
    product-form smart button 'Reordering Rules' therefore shows
    `0 Reordering Rules` and the list lands empty — the agent must click
    New and fill an inline row with Min=5 and Max=20.
  * Admin is granted `stock.group_stock_multi_locations` so the Location
    column is visible on the editable reordering-rules list (otherwise
    the column is hidden and the agent can't see that the default is
    WH/Stock — leaving them uncertain whether the row is correct).

The task difficulty is: Inventory > Products > open product > click the
'Reordering Rules' smart button (its label reads '0 Reordering Rules'
pre-task) > New > fill two numeric cells (product_min_qty=5,
product_max_qty=20) > Save. The agent must not confuse the Min/Max columns
with adjacent numeric columns such as `qty_to_order`, `qty_on_hand`, or
`qty_forecast`, and must not drop the product/location context when the
inline row opens (Odoo pre-fills from `default_product_id` injected by
action_view_orderpoints).
"""

PRODUCT_NAME = "Bench Reorder Item"


def _cleanup(env):
    # Remove any pre-existing orderpoints for the product (leftovers from
    # previous failed runs) and then the product itself.
    products = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if products:
        try:
            env["stock.warehouse.orderpoint"].with_context(
                active_test=False
            ).search([("product_id", "in", products.ids)]).unlink()
        except Exception:
            pass
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

    # Grant admin the multi-locations group so the Reordering Rules
    # editable-list view surfaces the Location column (WH/Stock default)
    # instead of silently hiding it. Also ensures the product form's
    # smart button section renders consistently for all users.
    admin = env.ref("base.user_admin")
    admin.group_ids |= env.ref("stock.group_stock_multi_locations")

    # Create the storable product with no reordering rules.
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
        "list_price": 25.0,
        "standard_price": 12.0,
        "sale_ok": True,
        "purchase_ok": True,
    })
    product = tmpl.product_variant_id

    # Sanity: ensure no orderpoint exists for this product yet.
    existing = env["stock.warehouse.orderpoint"].with_context(
        active_test=False
    ).search([("product_id", "=", product.id)])
    if existing:
        existing.unlink()

    # Force flush
    env.cr.execute("SELECT 1")
