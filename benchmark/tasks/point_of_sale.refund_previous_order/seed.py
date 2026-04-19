"""Seed for point_of_sale.refund_previous_order.

Provisions a POS register 'Bench Refund POS' with a tax-free product
'Bench Widget' priced at 10.00 and a dedicated cash payment method
('Bench Refund Cash'). Opens a session (leaving opening_control) and
creates one prior fully-paid cash order:

    Bench Widget x 3 @ 10.00 = 30.00, paid in cash.

The agent must later open that prior order from the Orders list,
refund ONE Bench Widget via the POS refund flow (reducing the refund
qty from 3 to 1), and register a -10.00 cash payment.

Hard pattern: non-default numpad interaction (changing refund qty) +
navigating to an existing order from the Orders list + processing
a negative-amount cash payment.
"""


CONFIG_NAME = "Bench Refund POS"
PRODUCT_NAME = "Bench Widget"
CASH_METHOD = "Bench Refund Cash"
CASH_JOURNAL = "Bench Refund Cash Journal"


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
        "code": "BREF01",
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
        "list_price": 10.0,
        "taxes_id": [(5, 0, 0)],
    })
    product.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})

    config = env["pos.config"].create({
        "name": CONFIG_NAME,
    })
    config.write({"payment_method_ids": [(6, 0, [cash_pm.id])]})

    # Open a session and move it out of opening_control with 0 opening cash.
    session = env["pos.session"].create({"config_id": config.id})
    session.set_opening_control(0, "")

    # Create the prior fully-paid cash order: Bench Widget x 3 @ 10.00 = 30.00.
    order = env["pos.order"].create({
        "name": "Bench Refund POS - 000001",
        "pos_reference": "BENCH-REFUND-01",
        "session_id": session.id,
        "config_id": config.id,
        "company_id": env.company.id,
        "pricelist_id": config.pricelist_id.id if config.pricelist_id else False,
        "amount_tax": 0.0,
        "amount_total": 30.0,
        "amount_paid": 0.0,
        "amount_return": 0.0,
        "lines": [(0, 0, {
            "name": PRODUCT_NAME,
            "full_product_name": PRODUCT_NAME,
            "product_id": product.id,
            "price_unit": 10.0,
            "qty": 3,
            "discount": 0.0,
            "tax_ids": [(6, 0, [])],
            "price_subtotal": 30.0,
            "price_subtotal_incl": 30.0,
        })],
    })

    wizard = env["pos.make.payment"].with_context(
        active_id=order.id, active_ids=[order.id]
    ).create({
        "amount": 30.0,
        "payment_method_id": cash_pm.id,
    })
    wizard.with_context(active_id=order.id, active_ids=[order.id]).check()
