"""Clean up artifacts from previous runs for stock.archive_old_product_set_inactive."""


PRODUCT_NAME = "Bench Archive Me"


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
