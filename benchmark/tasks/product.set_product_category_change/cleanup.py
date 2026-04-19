"""Cleanup for product.set_product_category_change."""


PRODUCT_NAME = "Bench Cat Item"
CATEGORY_NAME = "Office Supplies"


def cleanup(env):
    Template = env["product.template"].with_context(active_test=False)
    stale = Template.search([("name", "=", PRODUCT_NAME)])
    for tmpl in stale:
        if not tmpl.active:
            tmpl.active = True
        for variant in tmpl.product_variant_ids:
            if not variant.active:
                variant.active = True
    try:
        stale.unlink()
    except Exception:
        for tmpl in stale:
            tmpl.write({"active": False})

    # Don't unlink 'Office Supplies' — seed re-ensures it on each run, and
    # other tasks may rely on it. Leaving it is harmless.
