"""Seed for inventory.cycle_count_two_locations_apply_selected_delta."""


PRODUCT_NAME = "Bench Cycle Count Rotor"


def setup(env):
    product = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if product:
        env["stock.quant"].search([("product_id", "in", product.ids)]).unlink()
        env["product.template"].search([("name", "=", PRODUCT_NAME)]).unlink()

    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "sale_ok": False,
        "purchase_ok": False,
        "list_price": 10.0,
    })
    product = tmpl.product_variant_id

    stock_loc = env["stock.location"].search([("complete_name", "=", "WH/Stock")], limit=1)
    input_loc = env["stock.location"].search([("complete_name", "=", "WH/Input")], limit=1)
    if not stock_loc or not input_loc:
        warehouse = env["stock.warehouse"].search([], limit=1)
        if not warehouse:
            raise RuntimeError("No warehouse found to attach inventory locations")
        parent = warehouse.view_location_id
        if not stock_loc:
            stock_loc = env["stock.location"].create({
                "name": "Stock",
                "location_id": parent.id,
                "usage": "internal",
            })
        if not input_loc:
            input_loc = env["stock.location"].create({
                "name": "Input",
                "location_id": parent.id,
                "usage": "internal",
            })

    quants = env["stock.quant"].with_context(inventory_mode=True).create([
        {
            "product_id": product.id,
            "location_id": stock_loc.id,
            "inventory_quantity": 10.0,
        },
        {
            "product_id": product.id,
            "location_id": input_loc.id,
            "inventory_quantity": 6.0,
        },
    ])
    quants.action_apply_inventory()
