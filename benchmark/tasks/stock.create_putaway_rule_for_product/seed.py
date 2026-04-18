"""Seed for stock.create_putaway_rule_for_product.

Category: deep_ui_interaction (HARD).

Prepares:
- Enables the Storage Locations feature (stock.group_stock_multi_locations)
  for the admin user so the 'Putaway Rules' menu and sub-location
  configuration become visible in the UI.
- Creates the storable product 'Bench Putaway Product'.
- Creates an internal sub-location WH/Stock/Bench Shelf A.
- Cleans up any leftover putaway rules for the product and prior sub-location
  from an earlier run.

The agent must then create a stock.putaway.rule routing
'Bench Putaway Product' arriving in WH/Stock to WH/Stock/Bench Shelf A.
"""


PRODUCT_NAME = "Bench Putaway Product"
SUBLOCATION_NAME = "Bench Shelf A"
SUBLOCATION_COMPLETE = "WH/Stock/Bench Shelf A"


def _get_stock_parent(env):
    loc = env["stock.location"].search(
        [("complete_name", "=", "WH/Stock"), ("usage", "=", "internal")],
        limit=1,
    )
    if not loc:
        loc = env["stock.location"].search(
            [("name", "=", "Stock"), ("usage", "=", "internal")], limit=1
        )
    if not loc:
        wh = env["stock.warehouse"].search([], limit=1)
        if not wh:
            raise RuntimeError("No warehouse found to attach the sub-location")
        loc = wh.lot_stock_id
    return loc


def setup(env):
    # --- Enable Storage Locations (multi-locations) feature ---
    # This surfaces the Putaway Rules menu under Configuration > Warehouse
    # and makes the stock.putaway.rule list editable.
    multi_loc_grp = env.ref(
        "stock.group_stock_multi_locations", raise_if_not_found=False
    )
    if multi_loc_grp:
        admin = env.ref("base.user_admin")
        if multi_loc_grp not in admin.group_ids:
            admin.group_ids = [(4, multi_loc_grp.id)]
        base_user = env.ref("base.group_user", raise_if_not_found=False)
        if base_user and multi_loc_grp not in base_user.implied_ids:
            base_user.implied_ids = [(4, multi_loc_grp.id)]

    # --- Cleanup prior runs ---
    # Remove any leftover putaway rules referring to the seeded product.
    existing_products = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)]
    )
    if existing_products:
        env["stock.putaway.rule"].search(
            [("product_id", "in", existing_products.ids)]
        ).unlink()
        # Drop quants then the product template to keep runs idempotent.
        env["stock.quant"].search(
            [("product_id", "in", existing_products.ids)]
        ).unlink()
        env["product.template"].search(
            [("name", "=", PRODUCT_NAME)]
        ).unlink()

    # Remove leftover sub-location(s) from prior runs.
    old_loc = env["stock.location"].search([("name", "=", SUBLOCATION_NAME)])
    if old_loc:
        # Any putaway rule still targeting it would block the unlink.
        env["stock.putaway.rule"].search(
            ["|",
             ("location_in_id", "in", old_loc.ids),
             ("location_out_id", "in", old_loc.ids)]
        ).unlink()
        env["stock.quant"].search(
            [("location_id", "in", old_loc.ids)]
        ).unlink()
        try:
            old_loc.unlink()
        except Exception:
            old_loc.write({"active": False})

    # --- Create the storable product ---
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,  # Odoo 19: storable = consu + is_storable=True
        "sale_ok": False,
        "purchase_ok": False,
        "list_price": 12.0,
    })
    product = tmpl.product_variant_id

    # --- Create the sub-location under WH/Stock ---
    parent = _get_stock_parent(env)
    env["stock.location"].create({
        "name": SUBLOCATION_NAME,
        "location_id": parent.id,
        "usage": "internal",
    })

    # --- Sanity checks ---
    target = env["stock.location"].search(
        [("complete_name", "=", SUBLOCATION_COMPLETE)], limit=1
    )
    assert target, (
        f"Seed failed: could not locate the freshly created "
        f"{SUBLOCATION_COMPLETE} location"
    )

    assert product.exists(), (
        f"Seed failed: product '{PRODUCT_NAME}' was not created"
    )

    assert not env["stock.putaway.rule"].search(
        [("product_id", "=", product.id)]
    ), (
        "Seed failed: a putaway rule already exists for "
        f"{PRODUCT_NAME}; the agent is supposed to create it."
    )
