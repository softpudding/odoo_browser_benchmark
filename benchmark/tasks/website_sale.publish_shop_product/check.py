"""Postcondition checks for website_sale.publish_shop_product."""


PRODUCT_NAME = "Shop Special Chair"
EXPECTED_TEXT = "Ergonomic task chair ready for the online shop."


def check(env):
    failures = []

    products = env["product.template"].search([("name", "=", PRODUCT_NAME)])
    if len(products) != 1:
        return [f"Expected exactly 1 product named '{PRODUCT_NAME}', found {len(products)}"]

    product = products[0]
    if abs(product.list_price - 199.0) > 0.0001:
        failures.append(f"Sales price is {product.list_price}, expected 199.0")
    if not product.is_published:
        failures.append("Product is not published to the website")
    if EXPECTED_TEXT not in (product.description_ecommerce or ""):
        failures.append("Website description does not contain the required text")

    return failures
