"""Seed a confirmed purchase order for the reset-to-draft edit re-confirm task.

Category 4: Recovery and rollback (EASY difficulty).
The PO is confirmed (state='purchase'). The agent must reset it to draft,
change the Terms and Conditions field, and re-confirm.
"""


def setup(env):
    # --- Cleanup prior runs ---
    vendor = env["res.partner"].search([("name", "=", "Meridian Supply Co")], limit=1)
    if vendor:
        old_pos = env["purchase.order"].search([
            ("partner_id", "=", vendor.id),
            ("name", "=", "BENCH-PO-RESET"),
        ])
        for po in old_pos:
            for pick in po.picking_ids.filtered(lambda p: p.state not in ("done", "cancel")):
                pick.action_cancel()
            if po.state in ("purchase", "done"):
                po.button_cancel()
            if po.state == "cancel":
                po.button_draft()
            po.unlink()

    # --- Create vendor if needed ---
    if not vendor:
        vendor = env["res.partner"].create({
            "name": "Meridian Supply Co",
            "email": "orders@meridian-supply.example.com",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": 1})

    # --- Create product if needed ---
    product = env["product.product"].search([("name", "=", "Rubber Gasket")], limit=1)
    if not product:
        tmpl = env["product.template"].create({
            "name": "Rubber Gasket",
            "type": "consu",
            "list_price": 1.50,
            "standard_price": 1.50,
        })
        product = tmpl.product_variant_id

    # --- Create confirmed PO with reference BENCH-PO-RESET ---
    po = env["purchase.order"].create({
        "partner_id": vendor.id,
        "name": "BENCH-PO-RESET",
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": product.id,
        "product_qty": 100,
        "price_unit": 1.50,
        "name": "Rubber Gasket",
    })
    po.button_confirm()
