"""Seed for stock.scrap_specific_serial_unit."""

PRODUCT_NAME = "Bench Sensor Module"
SERIALS = ["SN-A001", "SN-A002", "SN-A003"]


def setup(env):
    env["stock.scrap"].search([("product_id.display_name", "=", PRODUCT_NAME)]).unlink()
    env["stock.move.line"].search([("product_id.display_name", "=", PRODUCT_NAME)]).unlink()
    env["stock.move"].search([("product_id.display_name", "=", PRODUCT_NAME)]).unlink()
    env["stock.lot"].search([
        ("name", "in", SERIALS),
        ("product_id.display_name", "=", PRODUCT_NAME),
    ]).unlink()
    env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()

    admin = env.ref("base.user_admin")
    admin.group_ids |= env.ref("stock.group_production_lot")

    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "serial",
        "list_price": 90.0,
    })
    product = tmpl.product_variant_id

    warehouse = env["stock.warehouse"].search([], limit=1)
    stock_loc = warehouse.lot_stock_id

    for serial_name in SERIALS:
        lot = env["stock.lot"].create({
            "name": serial_name,
            "product_id": product.id,
        })
        env["stock.quant"].with_context(inventory_mode=True).create({
            "product_id": product.id,
            "location_id": stock_loc.id,
            "lot_id": lot.id,
            "inventory_quantity": 1.0,
        }).action_apply_inventory()
