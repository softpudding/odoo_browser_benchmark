"""Postcondition checks for website_sale.set_product_seo_title_meta."""


PRODUCT_NAME = "Bench SEO Widget"
EXPECTED_TITLE = "Buy Bench SEO Widget Online"
EXPECTED_DESCRIPTION = "Premium widget for benchmarking with fast delivery."


def check(env):
    failures = []

    products = env["product.template"].search([("name", "=", PRODUCT_NAME)])
    if len(products) != 1:
        return [f"Expected exactly 1 product named '{PRODUCT_NAME}', found {len(products)}"]

    product = products[0]
    if (product.website_meta_title or "").strip() != EXPECTED_TITLE:
        failures.append(
            f"website_meta_title is {product.website_meta_title!r}, expected {EXPECTED_TITLE!r}"
        )
    if (product.website_meta_description or "").strip() != EXPECTED_DESCRIPTION:
        failures.append(
            f"website_meta_description is {product.website_meta_description!r}, "
            f"expected {EXPECTED_DESCRIPTION!r}"
        )
    if not product.is_published:
        failures.append("Product was unpublished; it must stay published")
    if abs(product.list_price - 42.0) > 0.0001:
        failures.append(f"Product list_price changed to {product.list_price}; expected 42.0")

    return failures
