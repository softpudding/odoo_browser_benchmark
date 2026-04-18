"""Cleanup for pos_restaurant.open_table_order_mark_ready."""


CONFIG_NAME = "Bench Restaurant"
FLOOR_NAME = "Main Floor"
STARTER_NAME = "Starter Salad"
MAIN_NAME = "Main Steak"
CASH_METHOD = "Bench Resto Cash"


def cleanup(env):
    env["pos.order"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    env["pos.session"].search([("config_id.name", "=", CONFIG_NAME)]).unlink()
    configs = env["pos.config"].search([("name", "=", CONFIG_NAME)])
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
