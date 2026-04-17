"""Seed a confirmed sale order for cancel + recreate + send-email task.

Category 4: Recovery and rollback combined with policy trap.
The agent must cancel a confirmed SO (dialog), create a new quotation
with modified lines for a different customer (phantom empty line issue),
and send it by email via the compose wizard (complex modal).
"""

TARGET_REF = "BENCH-CANCEL-RESEND"
REPLACEMENT_REF = "CWS-REPLACE-01"


def setup(env):
    # --- Customers ---
    customers = {}
    for name, email in [
        ("Ironwood Distribution", "orders@ironwood-dist.example.com"),
        ("Clearwater Supply Co", "purchasing@clearwater-supply.example.com"),
    ]:
        partner = env["res.partner"].search([("name", "=", name)], limit=1)
        if not partner:
            partner = env["res.partner"].create({"name": name, "email": email})
        else:
            partner.write({"email": email})
        customers[name] = partner

    # --- Products ---
    products = {}
    for name, price in [
        ("Heavy-Duty Shelf Unit", 145.0),
        ("Packing Tape Industrial", 3.50),
    ]:
        product = env["product.product"].search([("name", "=", name)], limit=1)
        if not product:
            template = env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
                "invoice_policy": "order",
            })
            product = template.product_variant_id
        else:
            product.product_tmpl_id.write({
                "list_price": price,
                "invoice_policy": "order",
            })
        products[name] = product

    # --- Cleanup prior runs ---
    orders = env["sale.order"].search([
        ("client_order_ref", "in", [TARGET_REF, REPLACEMENT_REF]),
    ])
    for order in orders:
        if order.state == "sale":
            order.action_cancel()
        if order.state in ("draft", "cancel", "sent"):
            order.unlink()

    # --- Create confirmed SO for Ironwood Distribution ---
    order = env["sale.order"].create({
        "partner_id": customers["Ironwood Distribution"].id,
        "client_order_ref": TARGET_REF,
    })
    env["sale.order.line"].create({
        "order_id": order.id,
        "product_id": products["Heavy-Duty Shelf Unit"].id,
        "product_uom_qty": 12,
        "price_unit": 145.0,
        "name": "Heavy-Duty Shelf Unit",
        "tax_ids": [(5, 0, 0)],
    })
    env["sale.order.line"].create({
        "order_id": order.id,
        "product_id": products["Packing Tape Industrial"].id,
        "product_uom_qty": 150,
        "price_unit": 3.50,
        "name": "Packing Tape Industrial",
        "tax_ids": [(5, 0, 0)],
    })
    order.action_confirm()
