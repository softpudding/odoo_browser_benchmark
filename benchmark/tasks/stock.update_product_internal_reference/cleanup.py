"""Clean up artifacts from previous runs."""

PRODUCT_NAME = "Steel Bracket 12"


def cleanup(env):
    env["product.product"].search([("name", "=", PRODUCT_NAME)]).unlink()