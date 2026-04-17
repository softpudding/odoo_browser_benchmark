"""Seed data for purchase.cancel_rfq_log_note."""

VENDOR_NAME = "Blue Ridge Components"
TARGET_RFQ = "P-RFQ-CANCEL-01"
DISTRACTOR_RFQ = "P-RFQ-CANCEL-02"


def _ensure_vendor(env):
    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        vendor = env["res.partner"].create({
            "name": VENDOR_NAME,
            "supplier_rank": 1,
            "is_company": True,
        })
    else:
        vendor.write({"supplier_rank": max(vendor.supplier_rank, 1)})
    return vendor


def _ensure_product(env, name, price):
    product = env["product.product"].search([("name", "=", name)], limit=1)
    if product:
        product.product_tmpl_id.write({"standard_price": price, "purchase_ok": True})
        return product
    tmpl = env["product.template"].create({
        "name": name,
        "type": "consu",
        "purchase_ok": True,
        "standard_price": price,
    })
    return tmpl.product_variant_id


def _make_rfq(env, vendor, product, name):
    order = env["purchase.order"].create({
        "name": name,
        "partner_id": vendor.id,
    })
    env["purchase.order.line"].create({
        "order_id": order.id,
        "product_id": product.id,
        "name": product.name,
        "product_qty": 10,
        "price_unit": 42.0,
        "tax_ids": [(5, 0, 0)],
    })


def setup(env):
    orders = env["purchase.order"].search([("name", "in", [TARGET_RFQ, DISTRACTOR_RFQ])])
    if orders:
        env["mail.message"].search([
            ("model", "=", "purchase.order"),
            ("res_id", "in", orders.ids),
        ]).unlink()
        for order in orders:
            if order.state in ("purchase", "done"):
                order.button_cancel()
            order.unlink()

    vendor = _ensure_vendor(env)
    product = _ensure_product(env, "Precision Relay Pack", 42.0)
    _make_rfq(env, vendor, product, TARGET_RFQ)
    _make_rfq(env, vendor, product, DISTRACTOR_RFQ)
