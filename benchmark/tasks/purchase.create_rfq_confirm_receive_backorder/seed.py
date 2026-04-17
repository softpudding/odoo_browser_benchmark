"""Seed data for purchase.create_rfq_confirm_receive_backorder.

Hard task: Agent must create an RFQ from scratch with 3 product lines,
confirm the order, navigate to the receipt via smart button, set partial
done quantities, and choose Create Backorder in the validation dialog.
"""


def setup(env):
    # --- Vendor ---
    partner = env["res.partner"].search(
        [("name", "=", "Summit Ridge Components")], limit=1
    )
    if not partner:
        partner = env["res.partner"].create({
            "name": "Summit Ridge Components",
            "email": "orders@summitridgecomponents.com",
            "supplier_rank": 1,
        })
    else:
        partner.write({"supplier_rank": max(partner.supplier_rank, 1)})

    # --- Cleanup prior runs ---
    old_pos = env["purchase.order"].search([
        ("partner_ref", "=", "SRC-PO-2026-Q2"),
    ])
    for po in old_pos:
        # Cancel pickings linked to this PO first
        pickings = env["stock.picking"].search([
            ("origin", "=", po.name),
        ])
        for pk in pickings:
            if pk.state not in ("cancel", "done"):
                pk.action_cancel()
            pk.unlink()
        if po.state in ("purchase", "done"):
            po.button_cancel()
        po.unlink()

    # Also clean up any orphan pickings from prior runs
    old_pickings = env["stock.picking"].search([
        ("origin", "like", "SRC-PO-2026-Q2"),
    ])
    for pk in old_pickings:
        if pk.state not in ("cancel", "done"):
            pk.action_cancel()
        pk.unlink()

    # --- Products ---
    product_specs = [
        ("Hydraulic Cylinder 50mm", 85.00),
        ("Pressure Gauge PSI", 24.50),
        ("Flow Control Valve", 112.00),
    ]
    for name, price in product_specs:
        p = env["product.product"].search([("name", "=", name)], limit=1)
        if not p:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
                "standard_price": price,
                "purchase_ok": True,
                "taxes_id": [(5, 0, 0)],
                "supplier_taxes_id": [(5, 0, 0)],
            })
        else:
            p.product_tmpl_id.write({
                "list_price": price,
                "standard_price": price,
                "purchase_ok": True,
                "taxes_id": [(5, 0, 0)],
                "supplier_taxes_id": [(5, 0, 0)],
            })
