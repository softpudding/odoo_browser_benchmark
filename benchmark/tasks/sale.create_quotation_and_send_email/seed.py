"""Seed products and customer for a create-from-scratch + send-email task.

Category 2: Policy trap (wizard + create-from-scratch).
The agent must create a new SO with exact lines (proven hard — phantom
empty lines), then navigate the Send by Email compose wizard (complex
modal with template, recipients, subject, body).
"""


def setup(env):
    # --- Customer ---
    partner = env["res.partner"].search([("name", "=", "Riverton Supply Co.")], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": "Riverton Supply Co.",
            "email": "orders@riverton.example.com",
        })
    else:
        partner.write({"email": "orders@riverton.example.com"})

    # --- Products ---
    for name, price in [("Industrial Fan", 185.0), ("Air Filter Cartridge", 45.0)]:
        p = env["product.product"].search([("name", "=", name)], limit=1)
        if not p:
            env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
            })
        else:
            p.product_tmpl_id.write({"list_price": price})

    # --- Cleanup prior runs ---
    env["sale.order"].search([
        ("partner_id", "=", partner.id),
        ("state", "in", ("draft", "sent")),
    ]).unlink()
