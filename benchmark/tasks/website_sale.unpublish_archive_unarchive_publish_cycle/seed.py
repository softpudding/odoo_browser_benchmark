"""Seed a published+active eCommerce product for the unpublish/archive cycle task.

Category: deep_ui_interaction (medium).

The product starts in the *expected initial* state (published + active),
and the agent must walk it through:

    Unpublish -> Archive -> Unarchive -> Publish -> set internal reference

Because the final published/active state matches the initial state, the
verification anchor is the new ``default_code`` (``BCG-RESTORED``) the
agent must set in the last step. ``mail.message`` count is also bumped
by every transition, providing a behavioral signal in addition.
"""


PRODUCT_NAME = "Bench Cycle Gadget"


def setup(env):
    Product = env["product.template"].with_context(active_test=False)
    existing = Product.search([("name", "=", PRODUCT_NAME)])
    if existing:
        existing.unlink()

    Product.create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": False,
        "list_price": 79.0,
        "is_published": True,
        "website_published": True,
        "active": True,
        "default_code": "BCG-INIT",
        "description_ecommerce": "Original April 2026 gadget listing.",
    })
