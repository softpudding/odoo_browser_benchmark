"""Cleanup for website_sale.set_product_seo_title_meta."""


def cleanup(env):
    env["product.template"].with_context(active_test=False).search(
        [("name", "=", "Bench SEO Widget")]
    ).unlink()
