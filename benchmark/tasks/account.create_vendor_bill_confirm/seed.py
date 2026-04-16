"""Seed vendor and products for the create-vendor-bill-confirm task.

Category 2 (MEDIUM): Create a vendor bill from scratch with two product
lines, set bill date and reference, then confirm. Browser-use may struggle
with date picker and creating exact line items in accounting forms.
"""


def setup(env):
    # --- Cleanup prior runs ---
    old_bills = env["account.move"].search([
        ("ref", "=", "MSC-INV-4421"),
        ("move_type", "=", "in_invoice"),
    ])
    for bill in old_bills:
        if bill.state == "posted":
            bill.button_draft()
        bill.unlink()

    # --- Ensure vendor exists ---
    vendor = env["res.partner"].search(
        [("name", "=", "Meridian Supply Co")], limit=1
    )
    if not vendor:
        vendor = env["res.partner"].create({
            "name": "Meridian Supply Co",
            "email": "billing@meridiansupply.com",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": max(vendor.supplier_rank, 1)})

    # --- Ensure products exist ---
    for name, price in [("Cable Tray", 12.50), ("Junction Box", 8.00)]:
        product = env["product.product"].search(
            [("name", "=", name)], limit=1
        )
        if not product:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
                "standard_price": price,
            })
