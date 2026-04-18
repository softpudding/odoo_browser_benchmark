"""Postcondition checks for website_sale.unpublish_archive_unarchive_publish_cycle.

The task takes a published+active product through:
    Unpublish -> Archive -> Unarchive -> Publish -> set Internal Reference.

The verification anchor is the new ``default_code`` (``BCG-RESTORED``)
because the final published/active state matches the initial state.
``product.template`` does not track ``is_published`` / ``active`` on
mail.thread, so we verify the resulting field values directly rather
than counting chatter messages.
"""


PRODUCT_NAME = "Bench Cycle Gadget"
EXPECTED_CODE = "BCG-RESTORED"


def check(env):
    failures = []

    Product = env["product.template"].with_context(active_test=False)
    products = Product.search([("name", "=", PRODUCT_NAME)])
    if len(products) != 1:
        return [
            f"Expected exactly 1 product named '{PRODUCT_NAME}', found {len(products)}"
        ]

    product = products[0]

    if not product.active:
        failures.append(
            f"Product '{PRODUCT_NAME}' is archived; expected active=True"
        )
    if not product.is_published:
        failures.append(
            f"Product '{PRODUCT_NAME}' is not published; expected is_published=True"
        )
    if (product.default_code or "") != EXPECTED_CODE:
        failures.append(
            f"Product '{PRODUCT_NAME}' default_code is "
            f"{product.default_code!r}, expected {EXPECTED_CODE!r}"
        )

    return failures
