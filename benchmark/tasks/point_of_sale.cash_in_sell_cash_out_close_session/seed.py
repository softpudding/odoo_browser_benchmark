"""Seed for point_of_sale.cash_in_sell_cash_out_close_session."""


CONFIG_NAME = "Benchmark Cash Desk"
PRODUCT_NAME = "Bench Snack Crate"
CASH_METHOD = "Bench Cash"
CASH_JOURNAL = "Bench Cash Drawer"


def setup(env):
    env["pos.order"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.session"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.config"].search([("name", "=", CONFIG_NAME)]).unlink()
    env["pos.payment.method"].search([("name", "=", CASH_METHOD)]).unlink()
    env["account.journal"].search([("name", "=", CASH_JOURNAL)]).unlink()
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()

    receivable = (
        env.company.account_default_pos_receivable_account_id
        or env.company.partner_id.property_account_receivable_id
    )
    cash_journal = env["account.journal"].create({
        "name": CASH_JOURNAL,
        "type": "cash",
        "code": "BCD01",
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
        "list_price": 12.0,
        "taxes_id": [(5, 0, 0)],
    })
    product.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})

    config = env["pos.config"].create({
        "name": CONFIG_NAME,
        "cash_control": True,
    })
    config.write({"payment_method_ids": [(6, 0, [cash_pm.id])]})

    env["pos.session"].create({"config_id": config.id})
