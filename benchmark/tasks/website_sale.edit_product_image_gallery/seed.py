"""Seed a published website_sale product with no extra images.

The task asks the agent to add a single extra `product.image` gallery
entry named 'Bench Side View' via the product form's eCommerce Media
widget. We seed the product published with taxes cleared and no prior
images so the expected new record is unambiguous.
"""


PRODUCT_NAME = "Bench Gallery Mug"


def setup(env):
    # Clean up any prior runs (include archived/inactive).
    env["product.template"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    ).unlink()

    env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": 19.0,
        "is_published": True,
        "taxes_id": [(5, 0, 0)],
        "description_ecommerce": "<p>A sturdy ceramic mug used in benchmark calibration.</p>",
    })
