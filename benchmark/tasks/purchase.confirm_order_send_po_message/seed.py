"""Seed draft RFQs for the confirm-order-send-po-message task.

Category 2 (MEDIUM): Edit an RFQ, confirm it, then complete the Send PO
compose wizard with an exact subject and body.
"""

VENDOR_NAME = "Sterling Components"
TARGET_REF = "MED-SEND-PO-01"
DISTRACTOR_REF = "MED-SEND-PO-02"
TARGET_SUBJECT = "Sterling components order follow-up"


def _cleanup_purchase_orders(env, refs):
    pos = env["purchase.order"].search([("partner_ref", "in", refs)])
    for po in pos:
        if po.state in ("purchase", "done"):
            po.button_cancel()
        po.unlink()

    env["mail.message"].search([("subject", "=", TARGET_SUBJECT)]).unlink()


def _ensure_product(env, name, price):
    product = env["product.product"].search([("name", "=", name)], limit=1)
    if product:
        product.product_tmpl_id.write({
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


def _make_po(env, vendor, ref, breaker, labels):
    po = env["purchase.order"].create({
        "partner_id": vendor.id,
        "partner_ref": ref,
        "origin": ref,
    })

    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": breaker.id,
        "product_qty": 6,
        "price_unit": 48.0,
        "tax_ids": [(5, 0, 0)],
    })
    env["purchase.order.line"].create({
        "order_id": po.id,
        "product_id": labels.id,
        "product_qty": 2,
        "price_unit": 19.5,
        "tax_ids": [(5, 0, 0)],
    })
    return po


def setup(env):
    _cleanup_purchase_orders(env, [TARGET_REF, DISTRACTOR_REF])

    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        vendor = env["res.partner"].create({
            "name": VENDOR_NAME,
            "email": "ap@sterling-components.example.com",
            "supplier_rank": 1,
        })
    else:
        vendor.write({"supplier_rank": max(vendor.supplier_rank, 1)})

    breaker = _ensure_product(env, "Circuit Breaker Pack", 48.0)
    labels = _ensure_product(env, "Panel Label Set", 19.5)

    _make_po(env, vendor, TARGET_REF, breaker, labels)
    _make_po(env, vendor, DISTRACTOR_REF, breaker, labels)
