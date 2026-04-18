"""Seed for point_of_sale.add_item_apply_global_discount_pay_cash.

Installs pos_discount on demand, then provisions a POS register named
'Bench Test Store' configured to expose the global Discount control
button with a 15% default. Includes a single product priced at 20.0
(no tax) so that 2 units come to 40.00 and a 15% global discount lands
on exactly 34.00.
"""


CONFIG_NAME = "Bench Test Store"
PRODUCT_NAME = "Bench POS Widget"
CASH_METHOD = "Bench Cash"


def _ensure_pos_discount(env):
    mod = env["ir.module.module"].search([("name", "=", "pos_discount")], limit=1)
    if mod and mod.state != "installed":
        mod.button_immediate_install()


def setup(env):
    _ensure_pos_discount(env)

    # Cleanup prior runs (orders, sessions, then config). Use sudo to
    # bypass any access constraints introduced by pos_discount.
    env["pos.order"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.session"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.config"].search([("name", "=", CONFIG_NAME)]).unlink()
    env["pos.payment.method"].search([("name", "=", CASH_METHOD)]).unlink()
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()

    # Cash payment method using the company's default cash journal so
    # validation works without extra configuration.
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

    # Storable cleanly priced product, no tax so 2 x 20.00 = 40.00 and
    # 40.00 - 15% = 34.00 exactly.
    product = env["product.product"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "sale_ok": True,
        "available_in_pos": True,
        "list_price": 20.0,
        "taxes_id": [(5, 0, 0)],
    })
    product.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})

    # Discount product baked in by pos_discount data file. Fall back to
    # a fresh service product if the xmlid was somehow not loaded yet.
    discount_product = env.ref(
        "pos_discount.product_product_consumable",
        raise_if_not_found=False,
    )
    if not discount_product:
        discount_product = env["product.product"].create({
            "name": "Discount",
            "type": "service",
            "available_in_pos": False,
            "list_price": 0.0,
            "taxes_id": [(5, 0, 0)],
            "default_code": "DISC",
        })

    config = env["pos.config"].create({
        "name": CONFIG_NAME,
        "module_pos_discount": True,
        "iface_discount": True,
        "discount_pc": 15.0,
        "discount_product_id": discount_product.id,
    })
    config.write({"payment_method_ids": [(6, 0, [cash_pm.id])]})

    # Open a fresh session so the agent (and the JSON-RPC oracle) can
    # immediately create orders against it. The session starts in
    # 'opening_control' until the cash float is confirmed.
    env["pos.session"].create({"config_id": config.id})
