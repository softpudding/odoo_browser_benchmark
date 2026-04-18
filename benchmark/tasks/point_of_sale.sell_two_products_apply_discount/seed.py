"""Seed for point_of_sale.sell_two_products_apply_discount.

Provisions a POS register 'Bench Discount POS' with two tax-free products
(Bench POS Pen at €10 and Bench POS Notebook at €20) and a dedicated cash
payment method. A POS session is pre-opened so the oracle JSON-RPC script
(and the browser agent) can create orders against it right away.

Medium pattern: the agent must add two products, then apply a 10% discount
on a SPECIFIC line (the Notebook) via the on-screen % Disc numpad button
WITHOUT applying a global/whole-order discount, and finally pay cash for
€28.00.
"""


CONFIG_NAME = "Bench Discount POS"
PRODUCT_PEN = "Bench POS Pen"
PRODUCT_NOTEBOOK = "Bench POS Notebook"
CASH_METHOD = "Bench Discount Cash"


def _cleanup(env):
    env["pos.order"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.session"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.config"].search([("name", "=", CONFIG_NAME)]).unlink()
    env["pos.payment.method"].search([("name", "=", CASH_METHOD)]).unlink()
    env["product.template"].search([
        ("name", "in", [PRODUCT_PEN, PRODUCT_NOTEBOOK]),
    ]).unlink()


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

    # Two tax-free consumable products so math is exact:
    #   Pen      : 1 x 10.00       = 10.00
    #   Notebook : 1 x 20.00 - 10% = 18.00
    #   Total                      = 28.00
    pen = env["product.product"].create({
        "name": PRODUCT_PEN,
        "type": "consu",
        "sale_ok": True,
        "available_in_pos": True,
        "list_price": 10.0,
        "taxes_id": [(5, 0, 0)],
    })
    pen.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})

    notebook = env["product.product"].create({
        "name": PRODUCT_NOTEBOOK,
        "type": "consu",
        "sale_ok": True,
        "available_in_pos": True,
        "list_price": 20.0,
        "taxes_id": [(5, 0, 0)],
    })
    notebook.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})

    config = env["pos.config"].create({
        "name": CONFIG_NAME,
    })
    config.write({"payment_method_ids": [(6, 0, [cash_pm.id])]})

    # Open a fresh POS session so the agent (and the JSON-RPC oracle) can
    # immediately create orders against it.
    env["pos.session"].create({"config_id": config.id})
