"""Seed completed receipts for the purchase return wizard task.

Category 3: Side-effect trap.
The agent must open a completed receipt, launch the Return wizard, enter exact
quantities on only two rows, and validate the generated return transfer.
Browser-use often leaves extra rows non-zero or uses Return All.
"""


ORIGINS = ["RET-PO-07", "RET-PO-08"]


def _ensure_product(env, name, price):
    product = env["product.product"].search([("name", "=", name)], limit=1)
    if not product:
        tmpl = env["product.template"].create(
            {
                "name": name,
                "type": "consu",
                "is_storable": True,
                "list_price": price,
            }
        )
        product = tmpl.product_variant_id
    return product


def _cleanup_purchase_orders(env, vendor):
    orders = env["purchase.order"].search(
        [("partner_id", "=", vendor.id), ("origin", "in", ORIGINS)]
    )
    for po in orders:
        for pick in po.picking_ids.filtered(lambda p: p.state not in ("done", "cancel")):
            pick.action_cancel()
        if po.state in ("purchase", "done"):
            po.button_cancel()
        if po.state == "cancel":
            po.button_draft()
        po.unlink()


def _confirm_and_receive(po):
    po.button_confirm()
    receipt = po.picking_ids.filtered(lambda p: p.state not in ("cancel",))[:1]
    if receipt:
        for move in receipt.move_ids:
            move.quantity = move.product_uom_qty
        receipt.button_validate()


def setup(env):
    vendor = env["res.partner"].search(
        [("name", "=", "Harbor Precision Parts")], limit=1
    )
    if not vendor:
        vendor = env["res.partner"].create(
            {
                "name": "Harbor Precision Parts",
                "supplier_rank": 1,
                "email": "purchasing@harbor-precision.example.com",
            }
        )
    else:
        vendor.write({"supplier_rank": 1})

    _cleanup_purchase_orders(env, vendor)

    products = {
        "Servo Motor X2": _ensure_product(env, "Servo Motor X2", 120.0),
        "Sensor Harness Pro": _ensure_product(env, "Sensor Harness Pro", 35.0),
        "Panel Bracket 90": _ensure_product(env, "Panel Bracket 90", 18.0),
    }

    admin = env.ref("base.user_admin")

    target = env["purchase.order"].create(
        {
            "partner_id": vendor.id,
            "user_id": admin.id,
            "origin": "RET-PO-07",
            "order_line": [
                (0, 0, {"product_id": products["Servo Motor X2"].id, "product_qty": 6, "price_unit": 120.0, "date_planned": "2026-04-20 08:00:00"}),
                (0, 0, {"product_id": products["Sensor Harness Pro"].id, "product_qty": 4, "price_unit": 35.0, "date_planned": "2026-04-20 08:00:00"}),
                (0, 0, {"product_id": products["Panel Bracket 90"].id, "product_qty": 5, "price_unit": 18.0, "date_planned": "2026-04-20 08:00:00"}),
            ],
        }
    )
    _confirm_and_receive(target)

    distractor = env["purchase.order"].create(
        {
            "partner_id": vendor.id,
            "user_id": admin.id,
            "origin": "RET-PO-08",
            "order_line": [
                (0, 0, {"product_id": products["Servo Motor X2"].id, "product_qty": 3, "price_unit": 120.0, "date_planned": "2026-04-21 08:00:00"}),
                (0, 0, {"product_id": products["Sensor Harness Pro"].id, "product_qty": 2, "price_unit": 35.0, "date_planned": "2026-04-21 08:00:00"}),
            ],
        }
    )
    _confirm_and_receive(distractor)
