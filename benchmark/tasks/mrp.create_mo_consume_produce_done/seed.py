"""Seed products, stock, and a BoM for manufacturing-order creation."""


def setup(env):
    warehouse = env["stock.warehouse"].search([], limit=1)
    stock_loc = warehouse.lot_stock_id

    old_mos = env["mrp.production"].search([("product_id.display_name", "=", "Bench Power Pack")])
    for mo in old_mos:
        if mo.state != "cancel":
            mo.action_cancel()
        mo.unlink()
    env["mrp.bom"].search([("code", "=", "BOM-BPP-01")]).unlink()

    products = {}
    for name in ["Bench Power Pack", "Lithium Cell Module", "Control Board"]:
        product = env["product.product"].search([("name", "=", name)], limit=1)
        if not product:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "consu",
                "is_storable": True,
            })
            product = tmpl.product_variant_id
        products[name] = product

    env["stock.quant"]._update_available_quantity(products["Lithium Cell Module"], stock_loc, 50.0)
    env["stock.quant"]._update_available_quantity(products["Control Board"], stock_loc, 20.0)

    env["mrp.bom"].create({
        "code": "BOM-BPP-01",
        "product_tmpl_id": products["Bench Power Pack"].product_tmpl_id.id,
        "product_id": products["Bench Power Pack"].id,
        "product_qty": 1.0,
        "type": "normal",
        "consumption": "flexible",
        "bom_line_ids": [
            (0, 0, {"product_id": products["Lithium Cell Module"].id, "product_qty": 2.0}),
            (0, 0, {"product_id": products["Control Board"].id, "product_qty": 1.0}),
        ],
    })
