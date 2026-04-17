"""Seed a simple BoM for one-line quantity editing."""


def setup(env):
    env["mrp.bom"].search([("code", "=", "BOM-BENCH-MIXER")]).unlink()

    products = {}
    for name in ["Bench Mixer Assembly", "Motor Module", "Aluminum Housing"]:
        product = env["product.product"].search([("name", "=", name)], limit=1)
        if not product:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "consu",
                "is_storable": True,
            })
            product = tmpl.product_variant_id
        products[name] = product

    env["mrp.bom"].create({
        "code": "BOM-BENCH-MIXER",
        "product_tmpl_id": products["Bench Mixer Assembly"].product_tmpl_id.id,
        "product_id": products["Bench Mixer Assembly"].id,
        "product_qty": 1.0,
        "type": "normal",
        "bom_line_ids": [
            (0, 0, {"product_id": products["Motor Module"].id, "product_qty": 1.0}),
            (0, 0, {"product_id": products["Aluminum Housing"].id, "product_qty": 2.0}),
        ],
    })
