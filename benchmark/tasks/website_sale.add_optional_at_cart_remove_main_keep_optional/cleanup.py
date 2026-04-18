"""Cleanup for website_sale.add_optional_at_cart_remove_main_keep_optional."""

ORDER_REF = "BENCH-OPT-ORPHAN-01"
MAIN_NAME = "Bench Camera"
OPTIONAL_NAME = "Bench Tripod"


def cleanup(env):
    env["sale.order"].with_context(active_test=False).search([
        ("client_order_ref", "=", ORDER_REF),
    ]).sudo().unlink()
    admin = env.ref("base.user_admin")
    env["sale.order"].with_context(active_test=False).search([
        ("partner_id", "=", admin.partner_id.id),
        ("website_id", "!=", False),
        ("state", "=", "draft"),
    ]).sudo().unlink()
    env["product.template"].with_context(active_test=False).search([
        ("name", "in", [MAIN_NAME, OPTIONAL_NAME]),
    ]).sudo().unlink()
