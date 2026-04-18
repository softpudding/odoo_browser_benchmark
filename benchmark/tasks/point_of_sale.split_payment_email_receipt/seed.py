"""Seed for point_of_sale.split_payment_email_receipt."""


CONFIG_NAME = "Benchmark Bistro"
PRODUCT_NAME = "Harbor Granola Box"
PARTNER_NAME = "Harbor Receipt Customer"


def setup(env):
    env["pos.order"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.session"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.config"].search([("name", "=", CONFIG_NAME)]).unlink()
    env["pos.payment.method"].search([("name", "in", ["Bench Cash", "Bench Card"])]).unlink()
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()
    env["res.partner"].search([("name", "=", PARTNER_NAME)]).unlink()

    receivable = env.company.account_default_pos_receivable_account_id or env.company.partner_id.property_account_receivable_id
    cash_journal = env["account.journal"].search([("type", "=", "cash"), ("company_id", "=", env.company.id)], limit=1)
    bank_journal = env["account.journal"].search([("type", "=", "bank"), ("company_id", "=", env.company.id)], limit=1)

    cash_pm = env["pos.payment.method"].create({
        "name": "Bench Cash",
        "receivable_account_id": receivable.id,
        "journal_id": cash_journal.id,
    })
    card_pm = env["pos.payment.method"].create({
        "name": "Bench Card",
        "receivable_account_id": receivable.id,
        "journal_id": bank_journal.id,
    })

    product = env["product.product"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "sale_ok": True,
        "available_in_pos": True,
        "list_price": 9.6,
        "taxes_id": [(5, 0, 0)],
    })
    product.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})

    partner = env["res.partner"].create({
        "name": PARTNER_NAME,
        "email": "harbor.receipts@example.com",
        "customer_rank": 1,
    })

    config = env["pos.config"].create({"name": CONFIG_NAME})
    config.write({"payment_method_ids": [(6, 0, [cash_pm.id, card_pm.id])]})

    env["pos.session"].create({"config_id": config.id})
