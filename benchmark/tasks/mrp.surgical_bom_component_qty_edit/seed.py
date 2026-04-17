"""Seed for mrp.surgical_bom_component_qty_edit.

Creates a BOM for 'Benchmark Assembly Gamma' with 5 components. Task:
change the quantity of ONE specific component without touching others.
"""

FINISHED = "Benchmark Assembly Gamma"
COMPONENTS = [
    ("Gamma Frame", 1),
    ("Gamma Panel", 2),
    ("Gamma Bolt M6", 4),   # <-- this is the one to edit (4 → 6)
    ("Gamma Cable", 3),
    ("Gamma Sticker", 1),
]


def setup(env):
    Product = env["product.product"]
    BOM = env["mrp.bom"]

    # Clean prior runs.
    all_names = [FINISHED] + [c[0] for c in COMPONENTS]
    prior = Product.search([("name", "in", all_names)])
    prior_boms = BOM.search([
        ("product_tmpl_id", "in", prior.mapped("product_tmpl_id").ids),
    ])
    prior_boms.unlink()
    prior.mapped("product_tmpl_id").unlink()

    finished = Product.create({
        "name": FINISHED,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })

    comp_ids = []
    for name, _qty in COMPONENTS:
        p = Product.create({
            "name": name,
            "type": "consu",
            "is_storable": True,
            "tracking": "none",
        })
        comp_ids.append(p.id)

    bom_line_cmds = []
    for (name, qty), prod_id in zip(COMPONENTS, comp_ids):
        bom_line_cmds.append((0, 0, {"product_id": prod_id, "product_qty": qty}))

    BOM.create({
        "product_tmpl_id": finished.product_tmpl_id.id,
        "product_qty": 1,
        "type": "normal",
        "consumption": "flexible",
        "bom_line_ids": bom_line_cmds,
    })
