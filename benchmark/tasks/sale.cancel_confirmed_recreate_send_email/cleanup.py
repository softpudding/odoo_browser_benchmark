"""Clean up artifacts from previous runs."""


def cleanup(env):
    orders = env["sale.order"].search([
        ("client_order_ref", "in", ["BENCH-CANCEL-RESEND", "CWS-REPLACE-01"]),
    ])
    for order in orders:
        if order.state == "sale":
            order.action_cancel()
        if order.state in ("draft", "cancel", "sent"):
            order.unlink()

    # Clean up partners
    for name in ["Ironwood Distribution", "Clearwater Supply Co"]:
        partner = env["res.partner"].search([("name", "=", name)], limit=1)
        if partner:
            partner.unlink()

    # Clean up products
    for name in ["Heavy-Duty Shelf Unit", "Packing Tape Industrial"]:
        product = env["product.product"].search([("name", "=", name)], limit=1)
        if product:
            product.product_tmpl_id.unlink()
