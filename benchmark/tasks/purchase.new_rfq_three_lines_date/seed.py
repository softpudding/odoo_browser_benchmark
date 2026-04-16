"""Seed a vendor and products for the three-line RFQ creation task.

Category 5: Deep UI interaction.
The agent must create an RFQ from scratch with exactly three product lines
and a specific Order Deadline date set via the date picker widget. Browser-use
routinely leaves a phantom empty fourth line (it hits Enter after the last
line, creating a new empty row) and often fails to set the date picker
to the required value.
"""


def setup(env):
    # --- Cleanup prior runs ---
    vendor = env["res.partner"].search([("name", "=", "Meridian Supply Co")], limit=1)
    if vendor:
        old_pos = env["purchase.order"].search([("partner_id", "=", vendor.id)])
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

    # --- Create or find products ---
    product_specs = [
        ("Rubber Gasket", 1.50),
        ("Stainless Bolt M8", 0.75),
        ("Hex Nut M8", 0.40),
    ]
    for name, price in product_specs:
        p = env["product.product"].search([("name", "=", name)], limit=1)
        if not p:
            env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
                "standard_price": price,
            })
        else:
            p.product_tmpl_id.write({"standard_price": price})
