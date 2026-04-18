"""Seed a published website product with empty SEO metadata."""


PRODUCT_NAME = "Bench SEO Widget"


def setup(env):
    env["product.template"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    ).unlink()

    env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": 42.0,
        "is_published": True,
        "website_meta_title": False,
        "website_meta_description": False,
        "description_ecommerce": "<p>A sturdy bench widget used in benchmark calibration.</p>",
    })
