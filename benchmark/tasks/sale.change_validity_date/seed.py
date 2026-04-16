"""Seed a draft sale order for the validity_date change task.

Category: deep_ui_interaction (EASY).
Starting state: A single draft quotation for "Lakeview Partners" with
reference "BENCH-VALID-01", one product line, and validity_date set to
April 20, 2026. The agent must change it to May 15, 2026.
"""


def setup(env):
    # --- Cleanup prior runs ---
    env["sale.order"].search([("client_order_ref", "=", "BENCH-VALID-01")]).unlink()

    # --- Ensure partner exists ---
    partner = env["res.partner"].search([("name", "=", "Lakeview Partners")], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": "Lakeview Partners",
            "email": "contact@lakeviewpartners.com",
        })

    # --- Ensure a product exists ---
    product = env["product.product"].search([("name", "=", "Consulting Services")], limit=1)
    if not product:
        tmpl = env["product.template"].create({
            "name": "Consulting Services",
            "type": "service",
            "list_price": 150.0,
        })
        product = tmpl.product_variant_id

    # --- Create the target draft quotation ---
    admin = env.ref("base.user_admin")
    so = env["sale.order"].create({
        "partner_id": partner.id,
        "user_id": admin.id,
        "client_order_ref": "BENCH-VALID-01",
        "validity_date": "2026-04-20",
    })

    # --- Add one product line ---
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": product.id,
        "product_uom_qty": 10,
        "price_unit": 150.0,
    })
