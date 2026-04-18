"""Clean up artifacts created by seed.py or the agent run."""

PARTNER_NAME = "Bench Test Co"
TEMPLATE_NAME = "Bench Starter Pack"
PRODUCT_WIDGET = "Bench Widget"
PRODUCT_GADGET = "Bench Gadget"


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

    # --- Remove quotation template (and any SOs still pointing to it) ---
    template = env["sale.order.template"].with_context(active_test=False).search(
        [("name", "=", TEMPLATE_NAME)]
    )
    if template:
        orphan_orders = env["sale.order"].with_context(active_test=False).search([
            ("sale_order_template_id", "in", template.ids),
        ])
        for order in orphan_orders:
            if order.state == "sale":
                try:
                    order.action_cancel()
                except Exception:
                    pass
            order.sudo().unlink()
        template.sudo().unlink()

    # --- Remove products ---
    for pname in (PRODUCT_WIDGET, PRODUCT_GADGET):
        products = env["product.product"].with_context(active_test=False).search(
            [("name", "=", pname)]
        )
        if products:
            products.mapped("product_tmpl_id").sudo().unlink()

    # --- Remove partner ---
    if partner:
        partner.sudo().unlink()
