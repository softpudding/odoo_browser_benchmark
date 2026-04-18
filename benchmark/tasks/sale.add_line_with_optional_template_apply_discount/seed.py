"""Seed a draft quotation that the agent must extend with a new discounted line.

Starting state:
- Customer "Bench Optional Co" with a draft sale.order whose
  client_order_ref = "S-BENCH-OPT-001".
- One existing order line: "Bench Hardware Kit" qty 3 @ $120, 0% discount.
- "Bench Service Bundle" product exists in the catalog (storable=False / service)
  but is NOT on the quotation yet — the agent must add it.

The agent must add a new line for "Bench Service Bundle" with qty=2 and
discount=10%, and save without confirming.

Per-line discount column requires the sale.group_discount_per_so_line group
to be enabled on admin (otherwise the discount cell is hidden).
"""

ORDER_REF = "S-BENCH-OPT-001"
PARTNER_NAME = "Bench Optional Co"
EXISTING_PRODUCT = "Bench Hardware Kit"
NEW_PRODUCT = "Bench Service Bundle"


def setup(env):
    # Enable per-line discounts on admin so the Discount column is visible.
    discount_group = env.ref("sale.group_discount_per_so_line", raise_if_not_found=False)
    admin = env.ref("base.user_admin")
    if discount_group:
        admin.write({"group_ids": [(4, discount_group.id)]})

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": PARTNER_NAME,
            "email": "bench.optional@example.com",
        })

    # Cleanup any prior runs (handle non-draft state too).
    prior = env["sale.order"].with_context(active_test=False).search([
        ("partner_id", "=", partner.id),
        ("client_order_ref", "=", ORDER_REF),
    ])
    for order in prior:
        if order.state not in ("draft", "cancel"):
            try:
                order.action_cancel()
            except Exception:
                pass
        order.unlink()

    # Existing hardware kit (consumable).
    hw = env["product.product"].search([("name", "=", EXISTING_PRODUCT)], limit=1)
    if not hw:
        tmpl = env["product.template"].create({
            "name": EXISTING_PRODUCT,
            "type": "consu",
            "list_price": 120.0,
        })
        hw = tmpl.product_variant_id
    else:
        hw.product_tmpl_id.write({"list_price": 120.0})

    # The service bundle the agent will add.
    sb = env["product.product"].search([("name", "=", NEW_PRODUCT)], limit=1)
    if not sb:
        tmpl = env["product.template"].create({
            "name": NEW_PRODUCT,
            "type": "service",
            "list_price": 250.0,
        })
        sb = tmpl.product_variant_id
    else:
        sb.product_tmpl_id.write({"list_price": 250.0, "type": "service"})

    so = env["sale.order"].create({
        "partner_id": partner.id,
        "user_id": admin.id,
        "client_order_ref": ORDER_REF,
    })

    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": hw.id,
        "product_uom_qty": 3,
        "price_unit": 120.0,
        "discount": 0.0,
        "tax_ids": [(5, 0, 0)],
    })
