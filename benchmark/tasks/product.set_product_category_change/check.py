"""Postcondition checks for product.set_product_category_change.

Verifies that the seeded 'Bench Cat Item' product.template has its
categ_id pointing at the 'Office Supplies' product.category after the
agent saves the form. No other field on the product should change.
"""


PRODUCT_NAME = "Bench Cat Item"
CATEGORY_NAME = "Office Supplies"


def check(env):
    failures = []

    Template = env["product.template"].with_context(active_test=False)
    templates = Template.search([("name", "=", PRODUCT_NAME)])

    if len(templates) == 0:
        failures.append(
            f"Product template '{PRODUCT_NAME}' is missing — it must not "
            "be deleted, renamed, or archived."
        )
        return failures
    if len(templates) > 1:
        failures.append(
            f"Expected exactly 1 product.template named '{PRODUCT_NAME}'; "
            f"found {len(templates)}"
        )
        return failures

    tmpl = templates[0]

    if not tmpl.active:
        failures.append(
            f"Product '{PRODUCT_NAME}' must remain active (not archived)."
        )

    cat = env["product.category"].search([
        ("name", "=", CATEGORY_NAME),
    ], limit=1)
    if not cat:
        failures.append(
            f"Target category '{CATEGORY_NAME}' does not exist — seed "
            "should have created it."
        )
        return failures

    if tmpl.categ_id.id != cat.id:
        failures.append(
            f"Product '{PRODUCT_NAME}' has categ_id="
            f"{tmpl.categ_id.display_name!r} (id={tmpl.categ_id.id}); "
            f"expected '{CATEGORY_NAME}' (id={cat.id})."
        )

    return failures
