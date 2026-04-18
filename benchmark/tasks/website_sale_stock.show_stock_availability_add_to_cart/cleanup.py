"""Cleanup for website_sale_stock.show_stock_availability_add_to_cart."""


PRODUCT_NAME = "Bench Limited Stock"


def cleanup(env):
    # Drop any draft website cart that references the seeded product.
    tmpl = env["product.template"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)], limit=1,
    )
    if tmpl:
        env["sale.order"].with_context(active_test=False).search([
            ("website_id", "!=", False),
            ("state", "=", "draft"),
            ("order_line.product_template_id", "=", tmpl.id),
        ]).sudo().unlink()
        variants = tmpl.product_variant_ids
        if variants:
            env["stock.quant"].sudo().search(
                [("product_id", "in", variants.ids)]
            ).sudo().unlink()
        tmpl.sudo().unlink()

    # Also drop generic admin-owned website carts from a prior run.
    admin = env.ref("base.user_admin")
    env["sale.order"].with_context(active_test=False).search([
        ("partner_id", "=", admin.partner_id.id),
        ("website_id", "!=", False),
        ("state", "=", "draft"),
    ]).sudo().unlink()
