"""Cleanup for point_of_sale.close_session_reconcile_cash_diff."""


def cleanup(env):
    env["pos.order"].search([("config_id.name", "=", "Bench Close POS")]).unlink()
    env["pos.session"].search([("config_id.name", "=", "Bench Close POS")]).unlink()
    env["pos.config"].search([("name", "=", "Bench Close POS")]).unlink()
    env["pos.payment.method"].search([("name", "=", "Bench Close Cash")]).unlink()
    env["account.journal"].search([("name", "=", "Bench Close Cash Journal")]).unlink()
    env["product.template"].search([("name", "=", "Bench Close Product")]).unlink()
