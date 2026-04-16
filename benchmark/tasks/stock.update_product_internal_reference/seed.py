"""Seed a product for the update-internal-reference task.

Category: deep_ui_interaction (EASY).
Starting state: Product "Steel Bracket 12" with no internal reference.
The agent must set the Internal Reference to "SB-12-BENCH".
"""

PRODUCT_NAME = "Steel Bracket 12"


def setup(env):
    env["product.product"].search([("name", "=", PRODUCT_NAME)]).unlink()

    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "list_price": 10.0,
        "default_code": "",
    })