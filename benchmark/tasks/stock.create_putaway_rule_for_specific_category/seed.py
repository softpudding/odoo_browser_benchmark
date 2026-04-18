"""Seed for stock.create_putaway_rule_for_specific_category.

Category: deep_ui_interaction (HARD).

Set up the prerequisites for the agent to create a CATEGORY-level putaway rule:
- A sub-location "Refrigerator" under WH/Stock (so the destination location exists).
- A product category "Bench Cold Items" (the trigger for the rule).
- A storable product "Bench Frozen Salmon" attached to that category — this
  product should NOT have its own putaway rule (the rule is category-level).

Cleans up any prior putaway rules touching the seeded category, products, or
shelf so re-runs start fresh.
"""

CATEGORY_NAME = "Bench Cold Items"
PRODUCT_NAME = "Bench Frozen Salmon"
SHELF_NAME = "Refrigerator"
STOCK_COMPLETE = "WH/Stock"


def _cleanup(env):
    cat = env["product.category"].search([("name", "=", CATEGORY_NAME)], limit=1)
    if cat:
        env["stock.putaway.rule"].search([
            ("category_id", "=", cat.id)
        ]).unlink()
    prod = env["product.product"].search([("name", "=", PRODUCT_NAME)], limit=1)
    if prod:
        env["stock.putaway.rule"].search([
            ("product_id", "=", prod.id)
        ]).unlink()
    shelf = env["stock.location"].search([
        ("name", "=", SHELF_NAME),
        ("complete_name", "=", f"WH/Stock/{SHELF_NAME}"),
    ], limit=1)
    if shelf:
        env["stock.putaway.rule"].search([
            ("location_out_id", "=", shelf.id),
        ]).unlink()


def _ensure_stock_location(env):
    loc = env["stock.location"].search([
        ("complete_name", "=", STOCK_COMPLETE),
        ("usage", "=", "internal"),
    ], limit=1)
    if not loc:
        wh = env["stock.warehouse"].search([], limit=1)
        loc = wh.lot_stock_id
    return loc


def _ensure_shelf(env, parent_stock):
    shelf = env["stock.location"].search([
        ("name", "=", SHELF_NAME),
        ("location_id", "=", parent_stock.id),
    ], limit=1)
    if not shelf:
        shelf = env["stock.location"].create({
            "name": SHELF_NAME,
            "location_id": parent_stock.id,
            "usage": "internal",
        })
    return shelf


def _ensure_category(env):
    cat = env["product.category"].search([("name", "=", CATEGORY_NAME)], limit=1)
    if not cat:
        cat = env["product.category"].create({
            "name": CATEGORY_NAME,
        })
    return cat


def _ensure_product(env, name, category):
    product = env["product.product"].search([("name", "=", name)], limit=1)
    if not product:
        tmpl = env["product.template"].create({
            "name": name,
            "type": "consu",
            "is_storable": True,
            "list_price": 22.0,
            "categ_id": category.id,
        })
        product = tmpl.product_variant_id
    else:
        product.product_tmpl_id.write({
            "type": "consu",
            "is_storable": True,
            "categ_id": category.id,
        })
    return product


def setup(env):
    _cleanup(env)

    stock_loc = _ensure_stock_location(env)
    _ensure_shelf(env, stock_loc)

    cat = _ensure_category(env)
    # Add at least one product in the category so the category is meaningful;
    # the agent must NOT create a product-level rule for this product.
    _ensure_product(env, PRODUCT_NAME, cat)

    # Make sure stock multi-locations is enabled so the Putaway Rules menu
    # shows up. (It usually is in the benchmark base, but this is cheap.)
    grp = env.ref("stock.group_stock_multi_locations", raise_if_not_found=False)
    if grp:
        admin = env.ref("base.user_admin")
        if grp not in admin.group_ids:
            admin.group_ids = [(4, grp.id)]
