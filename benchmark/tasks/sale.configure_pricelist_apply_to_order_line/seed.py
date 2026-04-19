"""Seed for sale.configure_pricelist_apply_to_order_line.

Category: deep_ui_interaction (HARD).

Two-stage workflow:
  1. Agent builds a new product.pricelist ('Bench 10% Off') with one rule
     (compute_price='formula', base='list_price', price_discount=10,
     applied_on='3_global').
  2. Agent creates a new sale.order for customer 'Bench Price Co', picks
     that pricelist, and adds 1x 'Bench Price Item' so the SO line's
     price_unit is recomputed by `_compute_price_unit` to 180.00.

Seeded state:
- `product.group_product_pricelist` feature group enabled on both admin and
  user_root so (a) the Pricelists menu is visible, (b) the Pricelist field
  on the sale.order form is visible, (c) pricelist computations work during
  seed.
- Consumable product 'Bench Price Item' with list_price=200.00 and no taxes
  (clean math: 10% off 200 -> 180.00).
- Customer 'Bench Price Co' (no pre-assigned pricelist so the agent must
  pick the pricelist they built themselves).
- Cleanup removes any prior-run sale orders, pricelist, product and
  customer first to make the task idempotent.
"""

PARTNER_NAME = "Bench Price Co"
PRODUCT_NAME = "Bench Price Item"
PRICELIST_NAME = "Bench 10% Off"


def setup(env):
    # --- Enable the pricelist feature group on admin + user_root ---
    admin = env.ref("base.user_admin")
    root = env.ref("base.user_root")
    pricelist_group = env.ref("product.group_product_pricelist")
    pricelist_group.sudo().write({"user_ids": [(4, admin.id), (4, root.id)]})

    # --- Cleanup child-first ---
    partner = env["res.partner"].with_context(active_test=False).search(
        [("name", "=", PARTNER_NAME)], limit=1
    )
    if partner:
        old_orders = env["sale.order"].with_context(active_test=False).search([
            ("partner_id", "=", partner.id),
        ])
        for order in old_orders:
            if order.state == "sale":
                try:
                    order.action_cancel()
                except Exception:
                    pass
            order.sudo().unlink()

    # Remove prior pricelist (detach from any partner property first)
    old_pricelist = env["product.pricelist"].with_context(active_test=False).search(
        [("name", "=", PRICELIST_NAME)]
    )
    if old_pricelist:
        # Also remove orphan SOs that reference this pricelist (any partner)
        orphan_orders = env["sale.order"].with_context(active_test=False).search([
            ("pricelist_id", "in", old_pricelist.ids),
        ])
        for order in orphan_orders:
            if order.state == "sale":
                try:
                    order.action_cancel()
                except Exception:
                    pass
            order.sudo().unlink()
        partners_with = env["res.partner"].with_context(active_test=False).search([
            ("specific_property_product_pricelist", "in", old_pricelist.ids),
        ])
        for p in partners_with:
            p.sudo().write({"specific_property_product_pricelist": False})
        old_pricelist.sudo().unlink()

    # Remove prior product
    old_product = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    )
    if old_product:
        old_product.mapped("product_tmpl_id").sudo().unlink()

    # Remove prior partner last (after orders are gone)
    if partner:
        partner.sudo().unlink()

    # --- Create product (no taxes -> clean math) ---
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "list_price": 200.0,
        "sale_ok": True,
        "taxes_id": [(5, 0, 0)],
    })
    tmpl.product_variant_id.product_tmpl_id.supplier_taxes_id = [(5, 0, 0)]

    # --- Create customer (no pre-assigned pricelist) ---
    env["res.partner"].create({
        "name": PARTNER_NAME,
        "email": "bench.price@example.com",
    })
