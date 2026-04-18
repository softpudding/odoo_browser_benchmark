"""Clean up artifacts created by seed.py or the agent run."""


def cleanup(env):
    # --- Remove orders for both test customers ---
    for customer_name in ("Bench Premium Co", "Bench Regular Co"):
        partner = env["res.partner"].with_context(active_test=False).search(
            [("name", "=", customer_name)], limit=1
        )
        if partner:
            orders = env["sale.order"].with_context(active_test=False).search([
                ("partner_id", "=", partner.id),
            ])
            for order in orders:
                if order.state == "sale":
                    order.action_cancel()
                order.sudo().unlink()
            partner.sudo().unlink()

    # --- Remove pricelist (detach first) ---
    pricelist = env["product.pricelist"].with_context(active_test=False).search(
        [("name", "=", "VIP 20% Off")]
    )
    if pricelist:
        partners_with = env["res.partner"].with_context(active_test=False).search([
            ("specific_property_product_pricelist", "in", pricelist.ids),
        ])
        for p in partners_with:
            p.sudo().write({"specific_property_product_pricelist": False})
        pricelist.sudo().unlink()

    # --- Remove product ---
    product = env["product.product"].with_context(active_test=False).search(
        [("name", "=", "Bench Standard Widget")]
    )
    if product:
        product.mapped("product_tmpl_id").sudo().unlink()
