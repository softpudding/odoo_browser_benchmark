"""Cleanup for point_of_sale.cash_in_sell_cash_out_close_session."""


def cleanup(env):
    env["pos.order"].search([("config_id.name", "=", "Benchmark Cash Desk")]).unlink()
    env["pos.session"].search([("config_id.name", "=", "Benchmark Cash Desk")]).unlink()
    env["pos.config"].search([("name", "=", "Benchmark Cash Desk")]).unlink()
    env["pos.payment.method"].search([("name", "=", "Bench Cash")]).unlink()
    env["account.journal"].search([("name", "=", "Bench Cash Drawer")]).unlink()
    env["product.template"].search([("name", "=", "Bench Snack Crate")]).unlink()
