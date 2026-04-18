"""Cleanup for point_of_sale.split_payment_email_receipt."""


def cleanup(env):
    env["pos.order"].search([("config_id.name", "=", "Benchmark Bistro")]).unlink()
    env["pos.session"].search([("config_id.name", "=", "Benchmark Bistro")]).unlink()
    env["pos.config"].search([("name", "=", "Benchmark Bistro")]).unlink()
    env["pos.payment.method"].search([("name", "in", ["Bench Cash", "Bench Card"])]).unlink()
    env["product.template"].search([("name", "=", "Harbor Granola Box")]).unlink()
    env["res.partner"].search([("name", "=", "Harbor Receipt Customer")]).unlink()
