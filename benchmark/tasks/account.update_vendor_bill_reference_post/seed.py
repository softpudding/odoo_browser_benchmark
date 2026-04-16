"""Seed draft vendor bills for the update-vendor-bill-reference-post task.

Category 3 (MEDIUM): open an existing draft vendor bill, edit a couple of
header fields plus one line quantity, then confirm without disturbing the
other line or the distractor bill.
"""

TARGET_REF = "MED-VB-DRAFT-01"
DISTRACTOR_REF = "MED-VB-DRAFT-02"
FINAL_REF = "MSC-8841"
VENDOR_NAME = "Meridian Supply Co"


def _cleanup_bills(env, refs):
    bills = env["account.move"].search([
        ("move_type", "=", "in_invoice"),
        ("ref", "in", refs),
    ])
    for bill in bills:
        if bill.state == "posted":
            bill.button_draft()
        bill.unlink()


def _ensure_product(env, name, price):
    product = env["product.product"].search([("name", "=", name)], limit=1)
    if product:
        product.product_tmpl_id.write({
            "list_price": price,
            "standard_price": price,
        })
        return product

    template = env["product.template"].create({
        "name": name,
        "type": "consu",
        "list_price": price,
        "standard_price": price,
    })
    return template.product_variant_id


def _make_bill(env, vendor, ref, cable, junction, cable_qty):
    return env["account.move"].create({
        "move_type": "in_invoice",
        "partner_id": vendor.id,
        "ref": ref,
        "invoice_date": "2026-04-29",
        "invoice_line_ids": [
            (0, 0, {
                "product_id": cable.id,
                "quantity": cable_qty,
                "price_unit": 12.5,
                "tax_ids": [(5, 0, 0)],
            }),
            (0, 0, {
                "product_id": junction.id,
                "quantity": 50,
                "price_unit": 8.0,
                "tax_ids": [(5, 0, 0)],
            }),
        ],
    })


def setup(env):
    _cleanup_bills(env, [TARGET_REF, DISTRACTOR_REF, FINAL_REF])

    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        vendor = env["res.partner"].create({
            "name": VENDOR_NAME,
            "email": "billing@meridian-supply.example.com",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": max(vendor.supplier_rank, 1)})

    cable = _ensure_product(env, "Cable Tray", 12.5)
    junction = _ensure_product(env, "Junction Box", 8.0)

    _make_bill(env, vendor, TARGET_REF, cable, junction, 40)
    _make_bill(env, vendor, DISTRACTOR_REF, cable, junction, 40)
