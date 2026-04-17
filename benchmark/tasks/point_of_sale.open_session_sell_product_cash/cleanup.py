"""Cleanup for point_of_sale.open_session_sell_product_cash."""


def cleanup(env):
    env["pos.order"].search([("config_id.name", "=", "Benchmark Counter")]).unlink()
    env["pos.session"].search([("config_id.name", "=", "Benchmark Counter")]).unlink()
    env["pos.config"].search([("name", "=", "Benchmark Counter")]).unlink()
    env["product.template"].search([("name", "=", "Counter Snack Box")]).unlink()
