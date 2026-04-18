"""Seed for point_of_sale.sell_pos_order_invoice_customer.

Provisions a POS register 'Bench Invoice POS' with one tax-free product
('Bench Invoice Item' priced at 50.00), a dedicated cash payment method,
a customer 'Invoice Iris' with a clean accounting setup, and an open
session ready for the agent to ring up an order.

Hard pattern: the agent must enable the Invoice toggle on the payment
screen (non-default — easy to miss) so that validation generates a
posted account.move customer invoice in Accounting.
"""


CONFIG_NAME = "Bench Invoice POS"
PRODUCT_NAME = "Bench Invoice Item"
CASH_METHOD = "Bench Invoice Cash"
PARTNER_NAME = "Invoice Iris"


def _cleanup(env):
    pos_orders = env["pos.order"].search([("config_id.name", "=", CONFIG_NAME)])
    moves = pos_orders.mapped("account_move")
    for mv in moves:
        if mv.state == "posted":
            try:
                mv.button_draft()
            except Exception:
                pass
        try:
            mv.unlink()
        except Exception:
            pass
    pos_orders.unlink()
    env["pos.session"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.config"].search([("name", "=", CONFIG_NAME)]).unlink()
    env["pos.payment.method"].search([("name", "=", CASH_METHOD)]).unlink()
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()
    env["res.partner"].search([("name", "=", PARTNER_NAME)]).unlink()


def setup(env):
    _cleanup(env)

    receivable = (
        env.company.account_default_pos_receivable_account_id
        or env.company.partner_id.property_account_receivable_id
    )
    cash_journal = env["account.journal"].search(
        [("type", "=", "cash"), ("company_id", "=", env.company.id)],
        limit=1,
    )
    cash_pm = env["pos.payment.method"].create({
        "name": CASH_METHOD,
        "receivable_account_id": receivable.id,
        "journal_id": cash_journal.id,
    })

    # Tax-free consumable priced for clean math (1 x 50.00 = 50.00).
    product = env["product.product"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "sale_ok": True,
        "available_in_pos": True,
        "list_price": 50.0,
        "taxes_id": [(5, 0, 0)],
    })
    product.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})

    env["res.partner"].create({
        "name": PARTNER_NAME,
        "email": "invoice.iris@example.com",
        "customer_rank": 1,
    })

    config = env["pos.config"].create({
        "name": CONFIG_NAME,
    })
    config.write({"payment_method_ids": [(6, 0, [cash_pm.id])]})

    env["pos.session"].create({"config_id": config.id})
