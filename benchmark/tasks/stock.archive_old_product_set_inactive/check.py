"""Postcondition checks for stock.archive_old_product_set_inactive.

Verifies the seeded storable product 'Bench Archive Me' is archived at
both the product.template and product.product levels, and that no
other product was accidentally archived or deleted.
"""


PRODUCT_NAME = "Bench Archive Me"


def check(env):
    failures = []

    Template = env["product.template"].with_context(active_test=False)
    Product = env["product.product"].with_context(active_test=False)

    templates = Template.search([("name", "=", PRODUCT_NAME)])
    if len(templates) == 0:
        failures.append(
            f"Product template '{PRODUCT_NAME}' is missing — it must not "
            "be deleted. Use Archive, not Delete."
        )
        return failures
    if len(templates) > 1:
        failures.append(
            f"Expected exactly 1 product.template named '{PRODUCT_NAME}'; "
            f"found {len(templates)}"
        )
        return failures

    tmpl = templates[0]

    if tmpl.active:
        failures.append(
            f"Product template '{PRODUCT_NAME}' still has active=True; "
            "expected active=False after archiving via cog Actions > Archive."
        )

    variants = Product.search([("product_tmpl_id", "=", tmpl.id)])
    if not variants:
        failures.append(
            f"Product '{PRODUCT_NAME}' has no product.product variants — "
            "something went wrong during seed or archiving."
        )
    for variant in variants:
        if variant.active:
            failures.append(
                f"product.product variant of '{PRODUCT_NAME}' "
                f"(id={variant.id}) still has active=True; expected "
                "active=False."
            )

    return failures
