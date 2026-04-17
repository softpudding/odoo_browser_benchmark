"""Seed a normal-type BOM that the agent must convert to Kit.

Easy: single field change on a well-named BOM.
"""


def setup(env):
    BOM = env["mrp.bom"]
    BOMLine = env["mrp.bom.line"]
    Product = env["product.product"]

    finished_name = "Benchmark Modular Shelving"
    comp_names = ["Bench Shelf Panel", "Bench Shelf Bracket", "Bench Shelf Screw"]

    # --- Cleanup prior runs ---
    stale_prod = Product.search([("name", "in", [finished_name] + comp_names)])
    if stale_prod:
        stale_bom = BOM.search([
            ("product_tmpl_id", "in", stale_prod.mapped("product_tmpl_id").ids),
        ])
        stale_bom.unlink()
        stale_prod.mapped("product_tmpl_id").unlink()

    # --- Create finished product ---
    finished = Product.create({
        "name": finished_name,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })

    # --- Create components ---
    comp_a = Product.create({
        "name": comp_names[0],
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    comp_b = Product.create({
        "name": comp_names[1],
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    comp_c = Product.create({
        "name": comp_names[2],
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })

    # --- Create BOM with type='normal' ---
    bom = BOM.create({
        "product_tmpl_id": finished.product_tmpl_id.id,
        "product_qty": 1,
        "type": "normal",
        "consumption": "flexible",
    })
    BOMLine.create({"bom_id": bom.id, "product_id": comp_a.id, "product_qty": 2})
    BOMLine.create({"bom_id": bom.id, "product_id": comp_b.id, "product_qty": 4})
    BOMLine.create({"bom_id": bom.id, "product_id": comp_c.id, "product_qty": 8})
