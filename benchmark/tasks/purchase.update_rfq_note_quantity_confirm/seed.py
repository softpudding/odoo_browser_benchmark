"""Seed RFQs for purchase.update_rfq_note_quantity_confirm."""

VENDOR_NAME = "North Coast Components"
TARGET_REF = "MED-RFQ-NOTE-01"
DISTRACTOR_REF = "MED-RFQ-NOTE-02"


def _cleanup_orders(env):
    orders = env["purchase.order"].search([
        "|",
        ("partner_ref", "in", [TARGET_REF, DISTRACTOR_REF]),
        ("origin", "in", [TARGET_REF, DISTRACTOR_REF]),
    ])
    for order in orders:
        if order.state in ("purchase", "done"):
            order.button_cancel()
        order.unlink()


def _ensure_product(env, name, price):
    product = env["product.product"].search([("name", "=", name)], limit=1)
    if product:
        product.product_tmpl_id.write({"list_price": price, "standard_price": price})
        return product
    template = env["product.template"].create({
        "name": name,
        "type": "consu",
        "list_price": price,
        "standard_price": price,
    })
    return template.product_variant_id


def _make_rfq(env, vendor, ref, dock_kit):
    return env["purchase.order"].create({
        "partner_id": vendor.id,
        "partner_ref": ref,
        "origin": ref,
        "note": "Keep original receiving instructions.",
        "order_line": [(0, 0, {
            "product_id": dock_kit.id,
            "product_qty": 18,
            "price_unit": 85.0,
            "date_planned": "2026-05-12 08:00:00",
            "tax_ids": [(5, 0, 0)],
        })],
    })


def setup(env):
    _cleanup_orders(env)
    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        vendor = env["res.partner"].create({
            "name": VENDOR_NAME,
            "email": "purchasing@northcoast.example.com",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": max(vendor.supplier_rank, 1)})
    dock_kit = _ensure_product(env, "Dock Seal Kit", 85.0)
    _make_rfq(env, vendor, TARGET_REF, dock_kit)
    _make_rfq(env, vendor, DISTRACTOR_REF, dock_kit)
