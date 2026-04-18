"""Seed for point_of_sale.attach_customer_apply_loyalty.

Provisions a POS register named 'Bench Loyalty POS' with a single tax-free
product priced at 20.00, a dedicated cash payment method, a loyalty program
that rewards a 10% order discount for 50 points, and a customer 'Loyal Larry'
who already holds a loyalty.card with 100 points (enough for 1 redemption,
not enough for 2).

Hard pattern: the agent must attach the customer mid-sale, open the Rewards
popup inside the POS kiosk UI, and redeem the points-funded discount reward
before paying cash.
"""


CONFIG_NAME = "Bench Loyalty POS"
PRODUCT_NAME = "Bench POS Item"
CASH_METHOD = "Bench Loyalty Cash"
PROGRAM_NAME = "Bench Loyalty Program"
PARTNER_NAME = "Loyal Larry"
REWARD_DESCRIPTION = "10% on your order"


def _cleanup(env):
    env["pos.order"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.session"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.config"].search([("name", "=", CONFIG_NAME)]).unlink()
    env["pos.payment.method"].search([("name", "=", CASH_METHOD)]).unlink()
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()

    # loyalty.program cannot be unlinked while active
    progs = env["loyalty.program"].with_context(active_test=False).search([
        ("name", "=", PROGRAM_NAME),
    ])
    cards = env["loyalty.card"].with_context(active_test=False).search([
        ("program_id", "in", progs.ids),
    ])
    cards.unlink()
    if progs:
        progs.write({"active": False})
        progs.unlink()

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

    # Tax-free storable product priced for clean math (3 x 20.00 = 60.00).
    product = env["product.product"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "sale_ok": True,
        "available_in_pos": True,
        "list_price": 20.0,
        "taxes_id": [(5, 0, 0)],
    })
    product.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})

    partner = env["res.partner"].create({
        "name": PARTNER_NAME,
        "email": "loyal.larry@example.com",
        "customer_rank": 1,
    })

    config = env["pos.config"].create({
        "name": CONFIG_NAME,
    })
    config.write({"payment_method_ids": [(6, 0, [cash_pm.id])]})

    # Loyalty program: nominative loyalty cards, auto-trigger on any order,
    # discount reward (10% off the order) funded by 50 points. Scoped
    # explicitly to the new POS config so the card shows up there.
    program = env["loyalty.program"].create({
        "name": PROGRAM_NAME,
        "program_type": "loyalty",
        "trigger": "auto",
        "applies_on": "both",
        "pos_ok": True,
        "pos_config_ids": [(6, 0, [config.id])],
        "rule_ids": [(5, 0, 0), (0, 0, {
            "minimum_qty": 1,
            "minimum_amount": 0,
            "reward_point_mode": "order",
            "reward_point_amount": 1,
        })],
        "reward_ids": [(5, 0, 0), (0, 0, {
            "reward_type": "discount",
            "discount": 10,
            "discount_mode": "percent",
            "discount_applicability": "order",
            "required_points": 50,
            "description": REWARD_DESCRIPTION,
        })],
    })

    # Mint a loyalty.card for Larry with 100 points — enough for one 50-point
    # redemption, but not two. Use loyalty_no_mail to suppress welcome email
    # side effects that would otherwise pollute the state diff.
    env["loyalty.card"].with_context(
        loyalty_no_mail=True, action_no_send_mail=True
    ).create({
        "program_id": program.id,
        "partner_id": partner.id,
        "points": 100.0,
    })

    # Open a fresh POS session so the agent (and the JSON-RPC oracle) can
    # immediately create orders against it.
    env["pos.session"].create({"config_id": config.id})
