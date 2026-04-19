"""Clean up artifacts created by seed.py or the agent run."""

PARTNER_NAME = "Bench Price Co"
PRODUCT_NAME = "Bench Price Item"
PRICELIST_NAME = "Bench 10% Off"


def cleanup(env):
    # --- Remove orders for the test customer (any state) ---
    partner = env["res.partner"].with_context(active_test=False).search(
        [("name", "=", PARTNER_NAME)], limit=1
    )
    if partner:
        orders = env["sale.order"].with_context(active_test=False).search([
            ("partner_id", "=", partner.id),
        ])
        for order in orders:
            if order.state == "sale":
                try:
                    order.action_cancel()
                except Exception:
                    pass
            order.sudo().unlink()

    # --- Remove pricelist (and any SOs pointing to it) ---
    pricelist = env["product.pricelist"].with_context(active_test=False).search(
        [("name", "=", PRICELIST_NAME)]
    )
    if pricelist:
        orphan_orders = env["sale.order"].with_context(active_test=False).search([
            ("pricelist_id", "in", pricelist.ids),
        ])
        for order in orphan_orders:
            if order.state == "sale":
                try:
                    order.action_cancel()
                except Exception:
                    pass
            order.sudo().unlink()
        partners_with = env["res.partner"].with_context(active_test=False).search([
            ("specific_property_product_pricelist", "in", pricelist.ids),
        ])
        for p in partners_with:
            p.sudo().write({"specific_property_product_pricelist": False})
        pricelist.sudo().unlink()

    # --- Remove product ---
    product = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    )
    if product:
        product.mapped("product_tmpl_id").sudo().unlink()

    # --- Remove partner ---
    if partner:
        partner.sudo().unlink()
