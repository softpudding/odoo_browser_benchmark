"""Cleanup for website_sale.add_product_review_publish."""


PRODUCT_NAME = "Bench Review Item"


def cleanup(env):
    products = env["product.template"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    )
    if products:
        env["rating.rating"].sudo().search([
            ("res_model", "=", "product.template"),
            ("res_id", "in", products.ids),
        ]).unlink()
        env["mail.message"].sudo().search([
            ("model", "=", "product.template"),
            ("res_id", "in", products.ids),
        ]).unlink()
        products.unlink()
