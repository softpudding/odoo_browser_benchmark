"""Seed for point_of_sale.close_session_reconcile_cash_diff.

Provisions a POS register 'Bench Close POS' with cash control enabled,
a tax-free product priced at 100.00, and an already-open session that has
exactly one paid cash order of 100.00. The expected cash balance at
closing is therefore 100.00, but the operator must close the session
with a counted cash of 97.00 (drawer is €3 short), producing a
cash_register_difference of -3.00.
"""


CONFIG_NAME = "Bench Close POS"
PRODUCT_NAME = "Bench Close Product"
CASH_METHOD = "Bench Close Cash"
CASH_JOURNAL = "Bench Close Cash Journal"


def _cleanup(env):
    env["pos.order"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.session"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.config"].search([("name", "=", CONFIG_NAME)]).unlink()
    env["pos.payment.method"].search([("name", "=", CASH_METHOD)]).unlink()
    env["account.journal"].search([("name", "=", CASH_JOURNAL)]).unlink()
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()


def setup(env):
    _cleanup(env)

    receivable = (
        env.company.account_default_pos_receivable_account_id
        or env.company.partner_id.property_account_receivable_id
    )

    cash_journal = env["account.journal"].create({
        "name": CASH_JOURNAL,
        "type": "cash",
        "code": "BCLS01",
        "company_id": env.company.id,
    })

    cash_pm = env["pos.payment.method"].create({
        "name": CASH_METHOD,
        "receivable_account_id": receivable.id,
        "journal_id": cash_journal.id,
    })

    product = env["product.product"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "sale_ok": True,
        "available_in_pos": True,
        "list_price": 100.0,
        "taxes_id": [(5, 0, 0)],
    })
    product.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})

    config = env["pos.config"].create({
        "name": CONFIG_NAME,
        "cash_control": True,
    })
    config.write({"payment_method_ids": [(6, 0, [cash_pm.id])]})

    # Open a session and move it out of opening_control with 0 opening cash.
    session = env["pos.session"].create({"config_id": config.id})
    session.set_opening_control(0, "")

    # Create a paid pos.order with one €100 line, paid in cash.
    order = env["pos.order"].create({
        "name": "POS/BENCH/CLOSE01",
        "pos_reference": "BENCH-CLOSE-01",
        "session_id": session.id,
        "config_id": config.id,
        "company_id": env.company.id,
        "pricelist_id": config.pricelist_id.id if config.pricelist_id else False,
        "amount_tax": 0.0,
        "amount_total": 100.0,
        "amount_paid": 0.0,
        "amount_return": 0.0,
        "lines": [(0, 0, {
            "name": PRODUCT_NAME,
            "full_product_name": PRODUCT_NAME,
            "product_id": product.id,
            "price_unit": 100.0,
            "qty": 1,
            "discount": 0.0,
            "tax_ids": [(6, 0, [])],
            "price_subtotal": 100.0,
            "price_subtotal_incl": 100.0,
        })],
    })

    wizard = env["pos.make.payment"].with_context(
        active_id=order.id, active_ids=[order.id]
    ).create({
        "amount": 100.0,
        "payment_method_id": cash_pm.id,
    })
    wizard.with_context(active_id=order.id, active_ids=[order.id]).check()
