"""Seed for stock.adjust_inventory_with_location_filter.

Category: side_effect_trap (MEDIUM).

Sets up:
- Two internal sub-locations under WH/Stock: "Shelf A" and "Shelf B"
  (created if missing).
- One storable product "Bench Multi Loc Product" with initial on-hand
  of 50 at WH/Stock/Shelf A and 30 at WH/Stock/Shelf B.

The agent must change only the Shelf A quant to 42 via Physical Inventory;
the Shelf B quant must remain at 30.
"""


PRODUCT_NAME = "Bench Multi Loc Product"
SHELF_A = "Shelf A"
SHELF_B = "Shelf B"


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
            raise RuntimeError("No warehouse found to attach inventory locations")
        loc = wh.lot_stock_id
    return loc


def _ensure_shelf(env, parent, name):
    shelf = env["stock.location"].search([
        ("name", "=", name),
        ("location_id", "=", parent.id),
    ], limit=1)
    if not shelf:
        shelf = env["stock.location"].create({
            "name": name,
            "location_id": parent.id,
            "usage": "internal",
        })
    else:
        # Normalize fields in case a prior run set them odd.
        shelf.write({"usage": "internal", "active": True})
    return shelf


def setup(env):
    # --- Cleanup prior runs for this product ---
    existing = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if existing:
        env["stock.quant"].search([("product_id", "in", existing.ids)]).unlink()
        env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()

    # --- Locate WH/Stock and ensure Shelf A / Shelf B child locations ---
    parent = _get_stock_parent(env)
    shelf_a = _ensure_shelf(env, parent, SHELF_A)
    shelf_b = _ensure_shelf(env, parent, SHELF_B)

    # Make sure multi-locations are enabled so the Physical Inventory view
    # shows sub-locations.
    grp = env.ref("stock.group_stock_multi_locations", raise_if_not_found=False)
    if grp:
        admin = env.ref("base.user_admin")
        if grp not in admin.group_ids:
            admin.group_ids = [(4, grp.id)]

    # --- Create the storable product ---
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "sale_ok": False,
        "purchase_ok": False,
        "list_price": 12.0,
    })
    product = tmpl.product_variant_id

    # --- Seed quants: 50 on Shelf A, 30 on Shelf B ---
    # Mirror the pattern used by sibling stock tasks: create the quant with
    # an inventory_quantity then action_apply_inventory to commit on-hand.
    seeded = env["stock.quant"].with_context(inventory_mode=True).create([
        {
            "product_id": product.id,
            "location_id": shelf_a.id,
            "inventory_quantity": 50.0,
        },
        {
            "product_id": product.id,
            "location_id": shelf_b.id,
            "inventory_quantity": 30.0,
        },
    ])
    seeded.action_apply_inventory()

    # Sanity: confirm each seeded quant is the expected on-hand quantity.
    def _q(loc):
        rec = env["stock.quant"].search([
            ("product_id", "=", product.id),
            ("location_id", "=", loc.id),
        ], limit=1)
        return rec.quantity if rec else 0.0

    assert abs(_q(shelf_a) - 50.0) < 1e-4, (
        f"Seed failed: Shelf A quant = {_q(shelf_a)}, expected 50.0"
    )
    assert abs(_q(shelf_b) - 30.0) < 1e-4, (
        f"Seed failed: Shelf B quant = {_q(shelf_b)}, expected 30.0"
    )
