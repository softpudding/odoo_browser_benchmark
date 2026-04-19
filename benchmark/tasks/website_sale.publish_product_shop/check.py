"""Postcondition checks for website_sale.publish_product_shop."""


PRODUCT_NAME = "Bench Gadget Pro"


def check(env):
    failures = []

    products = env["product.template"].search([("name", "=", PRODUCT_NAME)])
    if len(products) != 1:
        return [f"Expected exactly 1 product named '{PRODUCT_NAME}', found {len(products)}"]

    product = products[0]
    if abs(product.list_price - 99.0) > 0.0001:
        failures.append(f"Sales price is {product.list_price}, expected 99.0")
    if not product.is_published:
        failures.append("Product is not published (is_published=False)")
    if not product.website_published:
        failures.append("Product is not published on the website (website_published=False)")

    return failures
