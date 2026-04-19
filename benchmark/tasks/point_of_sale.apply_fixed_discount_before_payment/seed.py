"""Seed for point_of_sale.apply_fixed_discount_before_payment.

Installs pos_discount on demand, then provisions a POS register named
'Bench POS' configured to expose the global Discount control button
with a pre-filled 14.29% default. Includes two tax-free products
priced 20.00 and 15.00 so the subtotal is 35.00 and a 14.29% global
discount lands on (approximately) -5.00 giving a total of 30.00.

Hard pattern: the agent must find the global Discount button (hidden
inside the ellipsis / Actions popup in Odoo 19), accept the pre-filled
14.29 percentage, and complete a cash payment.
"""


CONFIG_NAME = "Bench POS"
PRODUCT_A_NAME = "Bench POS Item A"
PRODUCT_B_NAME = "Bench POS Item B"
CASH_METHOD = "Bench Cash"


def _ensure_pos_discount(env):
    mod = env["ir.module.module"].search([("name", "=", "pos_discount")], limit=1)
    if mod and mod.state != "installed":
        mod.button_immediate_install()


def _cleanup(env):
    env["pos.order"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.session"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.config"].search([("name", "=", CONFIG_NAME)]).unlink()
    env["pos.payment.method"].search([("name", "=", CASH_METHOD)]).unlink()
    env["product.template"].search([
        ("name", "in", [PRODUCT_A_NAME, PRODUCT_B_NAME]),
    ]).unlink()


def setup(env):
    _ensure_pos_discount(env)
    _cleanup(env)

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

    # Two tax-free products so 20.00 + 15.00 = 35.00 exactly.
    product_a = env["product.product"].create({
        "name": PRODUCT_A_NAME,
        "type": "consu",
        "sale_ok": True,
        "available_in_pos": True,
        "list_price": 20.0,
        "taxes_id": [(5, 0, 0)],
    })
    product_a.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})
    product_b = env["product.product"].create({
        "name": PRODUCT_B_NAME,
        "type": "consu",
        "sale_ok": True,
        "available_in_pos": True,
        "list_price": 15.0,
        "taxes_id": [(5, 0, 0)],
    })
    product_b.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})

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

    # discount_pc = 14.29 so 14.29% of 35.00 = 5.0015 ≈ 5.00 and the popup
    # is pre-filled with the exact value the agent needs to accept.
    config = env["pos.config"].create({
        "name": CONFIG_NAME,
        "module_pos_discount": True,
        "iface_discount": True,
        "discount_pc": 14.29,
        "discount_product_id": discount_product.id,
    })
    config.write({"payment_method_ids": [(6, 0, [cash_pm.id])]})

    # Open a fresh session so the agent (and the JSON-RPC oracle) can
    # immediately create orders against it. The session starts in
    # 'opening_control' until the cash float is confirmed.
    env["pos.session"].create({"config_id": config.id})
