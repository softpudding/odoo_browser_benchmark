"""Clean up artifacts from sale.create_quotation_down_payment_invoice."""

PARTNER_NAME = "Ridgeline Automation"
PRODUCT_NAMES = ["Modular Conveyor Belt", "Safety Light Curtain"]


def cleanup(env):
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return

    # Delete invoices linked to this partner
    invoices = env["account.move"].search([
        ("partner_id", "=", partner.id),
        ("move_type", "=", "out_invoice"),
    ])
    for inv in invoices:
        if inv.state == "posted":
            inv.button_draft()
        if inv.state != "cancel":
            inv.button_cancel()
        inv.unlink()

    # Delete sale orders for this partner
    orders = env["sale.order"].search([("partner_id", "=", partner.id)])
    for order in orders:
        if order.state == "sale":
            order._action_cancel()
        if order.state != "cancel":
            order.action_cancel()
        order.unlink()

    # Delete products
    for name in PRODUCT_NAMES:
        product = env["product.product"].search([("name", "=", name)], limit=1)
        if product:
            tmpl = product.product_tmpl_id
            product.unlink()
            if tmpl.exists():
                tmpl.unlink()

    # Delete partner
    partner.unlink()
