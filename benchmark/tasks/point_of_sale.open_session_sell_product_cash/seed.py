"""Seed a POS config and one POS product for a spike task."""


CONFIG_NAME = "Benchmark Counter"
PRODUCT_NAME = "Counter Snack Box"


def setup(env):
    orders = env["pos.order"].search([("config_id.name", "=", CONFIG_NAME)])
    orders.unlink()

    sessions = env["pos.session"].search([("config_id.name", "=", CONFIG_NAME)])
    sessions.unlink()

    env["pos.config"].search([("name", "=", CONFIG_NAME)]).unlink()
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()

    env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "sale_ok": True,
        "available_in_pos": True,
        "list_price": 8.5,
    })

    env["pos.config"].create({"name": CONFIG_NAME})
