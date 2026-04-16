"""Seed a medium purchase-to-receipt workflow.

Category 1 (MEDIUM): confirm an RFQ in Purchase, open the generated receipt in
Inventory, receive the full quantities, and validate it.
"""

TARGET_VENDOR = "Pioneer Industrial Supply"
TARGET_SOURCE = "MED-RECV-PO-01"
DISTRACTOR_SOURCE = "MED-RECV-PO-02"


def _cleanup(env, vendor):
    orders = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "in", [TARGET_SOURCE, DISTRACTOR_SOURCE]),
    ])
    for po in orders:
        for pick in po.picking_ids.filtered(lambda p: p.state not in ("done", "cancel")):
            pick.action_cancel()
        if po.state in ("purchase", "done"):
            po.button_cancel()
        if po.state == "cancel":
            po.button_draft()
        po.unlink()


def _ensure_product(env, name, price):
    product = env["product.product"].search([("name", "=", name)], limit=1)
    if product:
        product.product_tmpl_id.write({
            "type": "consu",
            "list_price": price,
            "standard_price": price,
        })
        return product
    tmpl = env["product.template"].create({
        "name": name,
        "type": "consu",
        "list_price": price,
        "standard_price": price,
    })
    return tmpl.product_variant_id


def _make_rfq(env, vendor, source, lines):
    po = env["purchase.order"].create({
        "partner_id": vendor.id,
        "origin": source,
    })
    for product, qty, price in lines:
        env["purchase.order.line"].create({
            "order_id": po.id,
            "product_id": product.id,
            "product_qty": qty,
            "price_unit": price,
            "name": product.name,
        })
    return po


def setup(env):
    vendor = env["res.partner"].search([("name", "=", TARGET_VENDOR)], limit=1)
    if not vendor:
        vendor = env["res.partner"].create({
            "name": TARGET_VENDOR,
            "email": "purchasing@pioneer-industrial.example.com",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": 1})

    _cleanup(env, vendor)

    steel_cable = _ensure_product(env, "Steel Cable Reel", 85.0)
    safety_tape = _ensure_product(env, "Safety Tape Pack", 18.0)

    _make_rfq(
        env,
        vendor,
        TARGET_SOURCE,
        [
            (steel_cable, 12, 85.0),
            (safety_tape, 30, 18.0),
        ],
    )
    _make_rfq(
        env,
        vendor,
        DISTRACTOR_SOURCE,
        [
            (steel_cable, 5, 85.0),
            (safety_tape, 10, 18.0),
        ],
    )
