"""Seed data for account.partial_pay_vendor_bill_with_memo."""

VENDOR_NAME = "Summit Office Supply"
TARGET_REF = "VB-PARTIAL-01"
DISTRACTOR_REF = "VB-PARTIAL-02"
AMOUNT = 900.0


def _cleanup(env):
    bills = env["account.move"].search([
        ("move_type", "=", "in_invoice"),
        ("ref", "in", [TARGET_REF, DISTRACTOR_REF]),
    ])
    for bill in bills:
        for payment in bill._get_reconciled_payments():
            if payment.state == "posted":
                payment.action_draft()
            payment.unlink()
        if bill.state == "posted":
            bill.button_draft()
        if bill.state == "draft":
            bill.button_cancel()
        bill.unlink()

    env["account.payment"].search([("memo", "=", "PARTIAL-JUN-600")]).unlink()


def _ensure_vendor(env):
    partner = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": VENDOR_NAME,
            "is_company": True,
            "supplier_rank": 1,
            "email": "ap@summitoffice.example.com",
        })
    else:
        partner.write({"supplier_rank": max(partner.supplier_rank, 1)})
    return partner


def _ensure_product(env):
    product = env["product.product"].search([("name", "=", "Office Seating Bundle")], limit=1)
    if product:
        product.product_tmpl_id.write({
            "type": "consu",
            "standard_price": AMOUNT,
            "list_price": AMOUNT,
        })
        return product
    tmpl = env["product.template"].create({
        "name": "Office Seating Bundle",
        "type": "consu",
        "standard_price": AMOUNT,
        "list_price": AMOUNT,
        "purchase_ok": True,
    })
    return tmpl.product_variant_id


def _make_bill(env, vendor, product, ref):
    journal = env["account.journal"].search([("type", "=", "purchase")], limit=1)
    bill = env["account.move"].create({
        "move_type": "in_invoice",
        "partner_id": vendor.id,
        "journal_id": journal.id,
        "ref": ref,
        "invoice_date": "2026-06-01",
        "invoice_line_ids": [(0, 0, {
            "product_id": product.id,
            "quantity": 1,
            "price_unit": AMOUNT,
            "tax_ids": [(5, 0, 0)],
        })],
    })
    bill.action_post()


def setup(env):
    _cleanup(env)

    vendor = _ensure_vendor(env)
    product = _ensure_product(env)
    _make_bill(env, vendor, product, TARGET_REF)
    _make_bill(env, vendor, product, DISTRACTOR_REF)
