"""Seed for product.set_product_category_change.

Easy task: the agent opens the product form for 'Bench Cat Item' (seeded
with categ_id='All') and changes the Product Category many2one to the
seeded 'Office Supplies' category, then saves.

Seeds:
    * A 'Office Supplies' product.category (if missing).
    * A consu product 'Bench Cat Item' with categ_id = 'All'
      (the Odoo built-in root category).
"""


PRODUCT_NAME = "Bench Cat Item"
CATEGORY_NAME = "Office Supplies"
ROOT_CATEGORY_NAME = "All"


def _cleanup(env):
    """Reset stale state so re-runs are deterministic."""
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


def _ensure_root_category(env):
    """Return the 'All' root product.category (ships with Odoo)."""
    # product.product_category_all is the XMLID of the root 'All' category.
    root = env.ref("product.product_category_all", raise_if_not_found=False)
    if root:
        return root
    # Fallback — find a category with no parent.
    root = env["product.category"].search([
        ("name", "=", ROOT_CATEGORY_NAME),
        ("parent_id", "=", False),
    ], limit=1)
    if root:
        return root
    # Last-resort fallback (shouldn't happen in standard Odoo installs):
    return env["product.category"].search([], limit=1, order="id asc")


def _ensure_office_supplies(env):
    """Create the target 'Office Supplies' category if it doesn't exist."""
    cat = env["product.category"].search([
        ("name", "=", CATEGORY_NAME),
    ], limit=1)
    if not cat:
        cat = env["product.category"].create({
            "name": CATEGORY_NAME,
        })
    return cat


def setup(env):
    _cleanup(env)

    root = _ensure_root_category(env)
    _ensure_office_supplies(env)

    env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "list_price": 12.0,
        "standard_price": 6.0,
        "sale_ok": True,
        "purchase_ok": True,
        "default_code": "BENCH-CAT-01",
        "categ_id": root.id,
    })

    env.cr.execute("SELECT 1")
