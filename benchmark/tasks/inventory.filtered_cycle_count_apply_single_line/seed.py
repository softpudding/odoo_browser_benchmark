"""Seed for inventory.filtered_cycle_count_apply_single_line."""

PRODUCT = "Bench Cycle Rotor"
TARGET_LOC = "WH/Cycle Bin"
OTHER_LOC = "WH/Stock"


def _ensure_location(env, name, parent):
    loc = env["stock.location"].search([("complete_name", "=", name)], limit=1)
    if loc:
        return loc
    return env["stock.location"].create({
        "name": name.split("/")[-1],
        "location_id": parent.id,
        "usage": "internal",
    })


def _set_qty(env, product, location, qty):
    env["stock.quant"].with_context(inventory_mode=True).create({
        "product_id": product.id,
        "location_id": location.id,
        "inventory_quantity": qty,
    }).action_apply_inventory()


def setup(env):
    tmpl = env["product.template"].search([("name", "=", PRODUCT)])
    tmpl.unlink()
    wh = env["stock.warehouse"].search([], limit=1)
    stock = wh.lot_stock_id
    bin_loc = _ensure_location(env, TARGET_LOC, wh.view_location_id)
    product = env["product.product"].create({
        "name": PRODUCT,
        "type": "consu",
        "is_storable": True,
        "list_price": 42.0,
    })
    _set_qty(env, product, stock, 4.0)
    _set_qty(env, product, bin_loc, 7.0)
