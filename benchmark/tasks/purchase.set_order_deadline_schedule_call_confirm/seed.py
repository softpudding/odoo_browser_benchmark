"""Seed RFQs for the set-order-deadline-schedule-call-confirm task.

Category 2 (MEDIUM): edit one RFQ header field, schedule one activity, then
confirm it while leaving a similar distractor RFQ untouched.
"""

VENDOR_NAME = "Blue Peak Industrial"
TARGET_REF = "MED-RFQ-ACT-01"
DISTRACTOR_REF = "MED-RFQ-ACT-02"
TARGET_ACTIVITY = "Confirm dock appointment"


def _cleanup_orders(env):
    env["mail.activity"].search([("summary", "=", TARGET_ACTIVITY)]).unlink()

    orders = env["purchase.order"].search([
        ("partner_ref", "in", [TARGET_REF, DISTRACTOR_REF]),
    ])
    for order in orders:
        if order.state in ("purchase", "done"):
            order.button_cancel()
        order.unlink()


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


def _make_rfq(env, vendor, ref, dock_plate, tape):
    return env["purchase.order"].create({
        "partner_id": vendor.id,
        "partner_ref": ref,
        "origin": ref,
        "order_line": [
            (0, 0, {
                "product_id": dock_plate.id,
                "product_qty": 8,
                "price_unit": 115.0,
                "date_planned": "2026-05-10 08:00:00",
                "tax_ids": [(5, 0, 0)],
            }),
            (0, 0, {
                "product_id": tape.id,
                "product_qty": 12,
                "price_unit": 24.0,
                "date_planned": "2026-05-10 08:00:00",
                "tax_ids": [(5, 0, 0)],
            }),
        ],
    })


def setup(env):
    _cleanup_orders(env)

    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        vendor = env["res.partner"].create({
            "name": VENDOR_NAME,
            "email": "purchasing@bluepeak.example.com",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": max(vendor.supplier_rank, 1)})

    dock_plate = _ensure_product(env, "Dock Plate", 115.0)
    tape = _ensure_product(env, "Packing Tape Case", 24.0)

    _make_rfq(env, vendor, TARGET_REF, dock_plate, tape)
    _make_rfq(env, vendor, DISTRACTOR_REF, dock_plate, tape)
