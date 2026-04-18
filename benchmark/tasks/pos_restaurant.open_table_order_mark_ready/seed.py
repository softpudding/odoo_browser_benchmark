"""Seed for pos_restaurant.open_table_order_mark_ready.

Provisions a restaurant-style POS register 'Bench Restaurant' (with
module_pos_restaurant=True) containing a single floor 'Main Floor' with a
single table T1 (table_number=1). Two tax-free products are created so that
the agent can place a two-item order on the table without dealing with tax
totals: Starter Salad (15.00) and Main Steak (20.00). A dedicated cash
payment method is attached so the POS config validates. The session is
opened automatically so the agent can start the register immediately.

Hard pattern: the agent must click table T1 on the floor plan, add both
products with an intervening click on the 'Course' button to split the
order into two courses, then click the Send/Order action-pad button to
fire Course 1 to the kitchen (which flips restaurant.order.course.fired
to True -- the Odoo 19 'marked ready' signal). Payment is not required.
"""


CONFIG_NAME = "Bench Restaurant"
FLOOR_NAME = "Main Floor"
TABLE_NUMBER = 1
STARTER_NAME = "Starter Salad"
MAIN_NAME = "Main Steak"
CASH_METHOD = "Bench Resto Cash"


def _ensure_pos_restaurant(env):
    mod = env["ir.module.module"].search([("name", "=", "pos_restaurant")], limit=1)
    if mod and mod.state != "installed":
        mod.button_immediate_install()


def _cleanup(env):
    env["pos.order"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.session"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    configs = env["pos.config"].search([("name", "=", CONFIG_NAME)])
    # Detach floor from config before unlinking floor/tables (floor has a
    # UserError guard that blocks unlink while a non-closed session exists).
    if configs:
        configs.write({"floor_ids": [(5, 0, 0)]})
        configs.unlink()

    floors = env["restaurant.floor"].with_context(active_test=False).search([
        ("name", "=", FLOOR_NAME),
    ])
    tables = env["restaurant.table"].with_context(active_test=False).search([
        ("floor_id", "in", floors.ids),
    ])
    tables.unlink()
    floors.unlink()

    env["pos.payment.method"].search([("name", "=", CASH_METHOD)]).unlink()
    env["product.template"].search([
        ("name", "in", [STARTER_NAME, MAIN_NAME]),
    ]).unlink()


def setup(env):
    _ensure_pos_restaurant(env)
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

    # Two tax-free consumable products priced for clean math (15 + 20 = 35).
    starter = env["product.product"].create({
        "name": STARTER_NAME,
        "type": "consu",
        "sale_ok": True,
        "available_in_pos": True,
        "list_price": 15.0,
        "taxes_id": [(5, 0, 0)],
    })
    starter.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})

    main = env["product.product"].create({
        "name": MAIN_NAME,
        "type": "consu",
        "sale_ok": True,
        "available_in_pos": True,
        "list_price": 20.0,
        "taxes_id": [(5, 0, 0)],
    })
    main.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})

    # Create the restaurant POS config. Passing module_pos_restaurant=True at
    # create time triggers the `_setup_default_floor` hook which spawns a
    # default floor + single table -- we replace it immediately with our
    # own deterministic floor/table.
    config = env["pos.config"].create({
        "name": CONFIG_NAME,
        "module_pos_restaurant": True,
    })
    config.write({"payment_method_ids": [(6, 0, [cash_pm.id])]})

    # Detach the auto-created default floor/table (if any) and drop them so
    # the only visible floor is our deterministic 'Main Floor' with a single
    # table whose table_number is 1 (label 'T1' in the kiosk UI).
    auto_floors = config.floor_ids
    config.write({"floor_ids": [(5, 0, 0)]})
    auto_tables = env["restaurant.table"].search([("floor_id", "in", auto_floors.ids)])
    auto_tables.unlink()
    auto_floors.unlink()

    floor = env["restaurant.floor"].create({
        "name": FLOOR_NAME,
        "pos_config_ids": [(6, 0, [config.id])],
    })
    env["restaurant.table"].create({
        "table_number": TABLE_NUMBER,
        "floor_id": floor.id,
        "seats": 4,
        "shape": "square",
        "position_h": 120,
        "position_v": 120,
        "width": 130,
        "height": 130,
    })

    # Open a fresh POS session so the agent (and the JSON-RPC oracle) can
    # jump straight into the kiosk.
    env["pos.session"].create({"config_id": config.id})
