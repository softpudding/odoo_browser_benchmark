"""Seed finished stock and a BoM for an unbuild task."""


def setup(env):
    warehouse = env["stock.warehouse"].search([], limit=1)
    stock_loc = warehouse.lot_stock_id

    env["mrp.unbuild"].search([("product_id.display_name", "=", "Field Controller Kit")]).unlink()
    env["mrp.bom"].search([("code", "=", "BOM-FCK-UNBUILD")]).unlink()

    products = {}
    for name in ["Field Controller Kit", "Sensor Board", "Wiring Loom"]:
        product = env["product.product"].search([("name", "=", name)], limit=1)
        if not product:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "consu",
                "is_storable": True,
            })
            product = tmpl.product_variant_id
        products[name] = product

    env["stock.quant"]._update_available_quantity(products["Field Controller Kit"], stock_loc, 5.0)

    env["mrp.bom"].create({
        "code": "BOM-FCK-UNBUILD",
        "product_tmpl_id": products["Field Controller Kit"].product_tmpl_id.id,
        "product_id": products["Field Controller Kit"].id,
        "product_qty": 1.0,
        "type": "normal",
        "bom_line_ids": [
            (0, 0, {"product_id": products["Sensor Board"].id, "product_qty": 2.0}),
            (0, 0, {"product_id": products["Wiring Loom"].id, "product_qty": 1.0}),
        ],
    })
