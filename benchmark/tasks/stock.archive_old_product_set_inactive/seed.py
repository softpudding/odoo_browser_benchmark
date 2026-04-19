"""Seed an active storable product 'Bench Archive Me' for archive-via-cog task.

Easy task: agent opens Inventory > Products, opens the product form, and
clicks cog Actions > Archive. The seed creates a storable product in the
active state so the Archive action is visible in the cog menu.
"""


PRODUCT_NAME = "Bench Archive Me"


def _cleanup(env):
    """Remove any stale 'Bench Archive Me' products from prior runs."""
    Template = env["product.template"].with_context(active_test=False)
    stale_tmpls = Template.search([("name", "=", PRODUCT_NAME)])
    for tmpl in stale_tmpls:
        # Reactivate so cascading unlink can proceed cleanly
        if not tmpl.active:
            tmpl.active = True
        for variant in tmpl.product_variant_ids:
            if not variant.active:
                variant.active = True
    try:
        stale_tmpls.unlink()
    except Exception:
        # If there are residual references, just force archive & move on
        for tmpl in stale_tmpls:
            tmpl.write({"active": False})


def setup(env):
    _cleanup(env)

    # Odoo 19: 'consu' + is_storable=True gives a storable product.
    env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "active": True,
        "list_price": 42.0,
        "standard_price": 21.0,
        "sale_ok": True,
        "purchase_ok": True,
        "default_code": "BENCH-ARCH-01",
    })

    # Force flush
    env.cr.execute("SELECT 1")
