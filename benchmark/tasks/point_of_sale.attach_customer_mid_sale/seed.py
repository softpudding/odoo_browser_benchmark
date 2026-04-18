"""Seed for point_of_sale.attach_customer_mid_sale.

Provisions a POS register 'Bench Easy POS' with a tax-free product priced
at 15.00, a dedicated cash payment method, an existing customer
'Bench POS Easy Customer', and an already-open POS session ready for the
agent (and JSON-RPC oracle) to create an order against.

Easy pattern: the agent just has to add the product, click the Customer
button, select the seeded customer, and pay cash.
"""


CONFIG_NAME = "Bench Easy POS"
PRODUCT_NAME = "Bench Easy POS Item"
CASH_METHOD = "Bench Easy Cash"
PARTNER_NAME = "Bench POS Easy Customer"


def _cleanup(env):
    env["pos.order"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.session"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.config"].search([("name", "=", CONFIG_NAME)]).unlink()
    env["pos.payment.method"].search([("name", "=", CASH_METHOD)]).unlink()
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()
    env["res.partner"].search([("name", "=", PARTNER_NAME)]).unlink()


def setup(env):
    _cleanup(env)

    # Cash payment method using the company's default cash journal.
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

    # Tax-free consumable product priced for clean math (1 x 15.00 = 15.00).
    product = env["product.product"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "sale_ok": True,
        "available_in_pos": True,
        "list_price": 15.0,
        "taxes_id": [(5, 0, 0)],
    })
    product.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})

    env["res.partner"].create({
        "name": PARTNER_NAME,
        "email": "bench.easy.customer@example.com",
        "customer_rank": 1,
    })

    config = env["pos.config"].create({
        "name": CONFIG_NAME,
    })
    config.write({"payment_method_ids": [(6, 0, [cash_pm.id])]})

    # Open a fresh POS session so the agent (and the JSON-RPC oracle) can
    # immediately create orders against it.
    env["pos.session"].create({"config_id": config.id})
