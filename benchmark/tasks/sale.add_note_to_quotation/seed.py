"""Seed a draft sale order for the chatter note task.

Category: deep_ui_interaction (EASY).
Starting state: A single draft quotation for "Azure Interior" with
reference "BENCH-NOTE-01", one product line.
The agent must post an internal log note in the chatter.
"""


def setup(env):
    # --- Cleanup prior runs ---
    existing = env["sale.order"].search([("client_order_ref", "=", "BENCH-NOTE-01")])
    for so in existing:
        env["mail.message"].search([
            ("res_model", "=", "sale.order"),
            ("res_id", "=", so.id),
            ("subtype_id.name", "=", "Note"),
        ]).unlink()
    existing.unlink()

    # --- Ensure partner exists ---
    partner = env["res.partner"].search([("name", "=", "Azure Interior")], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": "Azure Interior",
            "email": "contact@azureinterior.com",
        })

    # --- Ensure a product exists ---
    product = env["product.product"].search([("name", "=", "Corner Desk Right Pedestal")], limit=1)
    if not product:
        tmpl = env["product.template"].create({
            "name": "Corner Desk Right Pedestal",
            "type": "product",
            "list_price": 120.0,
        })
        product = tmpl.product_variant_id

    # --- Create the target draft quotation ---
    admin = env.ref("base.user_admin")
    so = env["sale.order"].create({
        "partner_id": partner.id,
        "user_id": admin.id,
        "client_order_ref": "BENCH-NOTE-01",
    })

    # --- Add one product line ---
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": product.id,
        "product_uom_qty": 2,
        "price_unit": 120.0,
    })