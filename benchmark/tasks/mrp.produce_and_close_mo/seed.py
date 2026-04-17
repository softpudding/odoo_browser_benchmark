"""Seed a confirmed manufacturing order for the produce-and-close task.

Category 2 (MEDIUM): The agent must find a confirmed MO, click Produce All,
and handle any confirmation dialog. Capability tested: list navigation +
action button click + optional wizard handling.
"""


def setup(env):
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    BOMLine = env["mrp.bom.line"]
    Product = env["product.product"]

    # --- Cleanup prior runs ---
    stale_mo = MO.search([("name", "=", "WH/MO/BENCH-001")])
    if stale_mo:
        for mo in stale_mo:
            if mo.state == "done":
                mo.button_unbuild()  # won't work easily, just force cancel
            if mo.state not in ("draft", "cancel"):
                mo.action_cancel()
        stale_mo.unlink()

    # Also clean up products
    stale_prod = Product.search([
        ("name", "in", [
            "Benchmark Assembly X",
            "Bench Component Alpha",
            "Bench Component Beta",
        ]),
    ])
    # Delete BOMs first
    stale_bom = BOM.search([
        ("product_tmpl_id", "in", stale_prod.mapped("product_tmpl_id").ids),
    ])
    stale_bom.unlink()
    stale_prod.mapped("product_tmpl_id").unlink()

    # --- Create finished product ---
    finished = Product.create({
        "name": "Benchmark Assembly X",
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })

    # --- Create component products ---
    comp_alpha = Product.create({
        "name": "Bench Component Alpha",
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    comp_beta = Product.create({
        "name": "Bench Component Beta",
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })

    # --- Create BOM ---
    bom = BOM.create({
        "product_tmpl_id": finished.product_tmpl_id.id,
        "product_qty": 1,
        "type": "normal",
        "consumption": "flexible",
    })
    BOMLine.create({
        "bom_id": bom.id,
        "product_id": comp_alpha.id,
        "product_qty": 2,
    })
    BOMLine.create({
        "bom_id": bom.id,
        "product_id": comp_beta.id,
        "product_qty": 3,
    })

    # --- Create and confirm MO ---
    mo = MO.create({
        "name": "WH/MO/BENCH-001",
        "product_id": finished.id,
        "product_qty": 5,
        "bom_id": bom.id,
    })
    mo.action_confirm()
