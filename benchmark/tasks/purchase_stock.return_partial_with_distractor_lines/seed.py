"""Seed a fully-received PO with three product lines for the partial-return task.

Category 3: Side-effect trap.
The agent must open a completed receipt, launch the Return wizard, set
return qty=0 on TWO of three rows (the distractor lines) and qty=2 on only
ONE row (WidgetB), then validate the resulting return picking. Browser-use
typically misses the explicit zero on the auto-populated rows and ends up
returning all three products.
"""


ORIGIN = "P-BENCH-RET-001"


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
    else:
        product.product_tmpl_id.write({"type": "consu", "list_price": price})
        product.is_storable = True
    return product


def _cleanup(env, vendor):
    orders = env["purchase.order"].search(
        [("partner_id", "=", vendor.id), ("origin", "=", ORIGIN)]
    )
    for po in orders:
        for picking in po.picking_ids:
            returns = env["stock.picking"].search([("return_id", "=", picking.id)])
            for ret in returns:
                if ret.state not in ("cancel", "done"):
                    ret.action_cancel()
                ret.move_ids.write({"state": "cancel"})
                ret.write({"state": "cancel"})
                ret.unlink()
        for pick in po.picking_ids.filtered(lambda p: p.state not in ("done", "cancel")):
            pick.action_cancel()
        if po.state in ("purchase", "done"):
            po.button_cancel()
        if po.state == "cancel":
            po.button_draft()
        po.unlink()


def setup(env):
    vendor = env["res.partner"].search(
        [("name", "=", "Bayside Components Co.")], limit=1
    )
    if not vendor:
        vendor = env["res.partner"].create(
            {
                "name": "Bayside Components Co.",
                "supplier_rank": 1,
                "email": "purchasing@bayside-components.example.com",
            }
        )
    else:
        vendor.write({"supplier_rank": 1})

    _cleanup(env, vendor)

    products = {
        "Bayside WidgetA": _ensure_product(env, "Bayside WidgetA", 25.0),
        "Bayside WidgetB": _ensure_product(env, "Bayside WidgetB", 15.0),
        "Bayside WidgetC": _ensure_product(env, "Bayside WidgetC", 32.0),
    }

    admin = env.ref("base.user_admin")

    po = env["purchase.order"].create(
        {
            "partner_id": vendor.id,
            "user_id": admin.id,
            "origin": ORIGIN,
            "order_line": [
                (0, 0, {
                    "product_id": products["Bayside WidgetA"].id,
                    "product_qty": 10,
                    "price_unit": 25.0,
                    "date_planned": "2026-04-20 08:00:00",
                }),
                (0, 0, {
                    "product_id": products["Bayside WidgetB"].id,
                    "product_qty": 5,
                    "price_unit": 15.0,
                    "date_planned": "2026-04-20 08:00:00",
                }),
                (0, 0, {
                    "product_id": products["Bayside WidgetC"].id,
                    "product_qty": 8,
                    "price_unit": 32.0,
                    "date_planned": "2026-04-20 08:00:00",
                }),
            ],
        }
    )

    po.button_confirm()
    receipt = po.picking_ids.filtered(lambda p: p.state not in ("cancel",))[:1]
    if receipt:
        for move in receipt.move_ids:
            move.quantity = move.product_uom_qty
            move.picked = True
        receipt.with_context(skip_backorder=True).button_validate()
