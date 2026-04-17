"""Seed data for sale.create_quotation_down_payment_invoice.

Creates the customer and products needed. Cleans up any prior run artifacts.
"""

PARTNER_NAME = "Ridgeline Automation"
PRODUCT_1 = "Modular Conveyor Belt"
PRODUCT_2 = "Safety Light Curtain"
CLIENT_REF = "RA-DP-2026"


def _cleanup(env):
    """Remove artifacts from prior runs."""
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return

    # Find all sale orders for this partner
    orders = env["sale.order"].search([("partner_id", "=", partner.id)])
    for order in orders:
        # Delete associated invoices first
        for invoice in order.invoice_ids:
            if invoice.state == "posted":
                invoice.button_draft()
            if invoice.state != "cancel":
                invoice.button_cancel()
            invoice.unlink()
        # Cancel and delete the order
        if order.state == "sale":
            order._action_cancel()
        if order.state != "cancel":
            order.action_cancel()
        order.unlink()

    # Also clean up any orphan invoices for this partner
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


def _ensure_product(env, name, price):
    """Create or update a product with the given name and price."""
    product = env["product.product"].search([("name", "=", name)], limit=1)
    if product:
        product.product_tmpl_id.write({
            "type": "consu",
            "invoice_policy": "order",
            "list_price": price,
        })
        product.write({"taxes_id": [(5, 0, 0)]})
        return product

    tmpl = env["product.template"].create({
        "name": name,
        "type": "consu",
        "invoice_policy": "order",
        "list_price": price,
        "taxes_id": [(5, 0, 0)],
    })
    return tmpl.product_variant_id


def setup(env):
    _cleanup(env)

    # --- Customer ---
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": PARTNER_NAME,
            "email": "orders@ridgeline-automation.example.com",
        })

    # --- Products ---
    _ensure_product(env, PRODUCT_1, 1200.0)
    _ensure_product(env, PRODUCT_2, 350.0)
