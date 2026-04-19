"""Seed for purchase_stock.receive_partial_scrap_damaged_units."""

ORIGIN = "SCRAP-PO-07"
VENDOR_NAME = "Bench Harbor Supply"
PRODUCTS = {
    "Bench Control Valve": 48.0,
    "Bench Filter Cartridge": 12.0,
}


def _ensure_vendor(env):
    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        vendor = env["res.partner"].create({
            "name": VENDOR_NAME,
            "supplier_rank": 1,
            "email": "purchasing@benchharbor.test",
        })
    else:
        vendor.write({"supplier_rank": max(vendor.supplier_rank, 1)})
    return vendor


def _ensure_products(env):
    result = {}
    for name, price in PRODUCTS.items():
        product = env["product.product"].search([("name", "=", name)], limit=1)
        if not product:
            product = env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
                "standard_price": price,
            }).product_variant_id
        result[name] = product
    return result


def setup(env):
    vendor = _ensure_vendor(env)
    products = _ensure_products(env)

    # Best-effort cleanup of unfinished stale runs; leave completed historical
    # runs intact because done scraps / done pickings are intentionally
    # undeletable in Odoo.
    stale_orders = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "=", ORIGIN),
        ("state", "in", ["draft", "sent", "purchase"]),
    ])
    for po in stale_orders:
        for scrap in env["stock.scrap"].with_context(active_test=False).search([
            ("picking_id", "in", po.picking_ids.ids),
            ("state", "=", "draft"),
        ]):
            scrap.unlink()
        for picking in po.picking_ids.filtered(lambda p: p.state not in ("done", "cancel")):
            try:
                picking.action_cancel()
                picking.unlink()
            except Exception:
                pass
        try:
            if po.state == "purchase":
                po.button_cancel()
            if po.state == "cancel":
                po.button_draft()
            po.unlink()
        except Exception:
            pass

    po = env["purchase.order"].create({
        "partner_id": vendor.id,
        "origin": ORIGIN,
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": products["Bench Control Valve"].id,
        "product_qty": 6.0,
        "price_unit": 48.0,
        "name": "Bench Control Valve",
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": products["Bench Filter Cartridge"].id,
        "product_qty": 10.0,
        "price_unit": 12.0,
        "name": "Bench Filter Cartridge",
    })
    po.button_confirm()
