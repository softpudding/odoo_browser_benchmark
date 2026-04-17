"""Seed for mrp.produce_mo_partial_backorder.

Category: policy_trap (MEDIUM).
Seeds a confirmed MO for 10 units. The agent must change Quantity
Producing to 6 and, when the backorder dialog appears, choose Create
Backorder so the remaining 4 units are split into a new MO.
"""


def setup(env):
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    BOMLine = env["mrp.bom.line"]
    Product = env["product.product"]

    # --- Cleanup prior runs ---
    stale_mo = MO.search([
        "|",
        ("name", "=", "WH/MO/BENCH-PART-001"),
        ("name", "=like", "WH/MO/BENCH-PART-001-%"),
    ])
    for mo in stale_mo:
        if mo.state not in ("draft", "cancel"):
            try:
                mo.action_cancel()
            except Exception:
                pass
    stale_mo.unlink()

    stale_prod = Product.search([
        ("name", "in", [
            "Bench Chassis Z",
            "Bench Frame Panel",
            "Bench Bolt Pack",
        ]),
    ])
    stale_bom = BOM.search([
        ("product_tmpl_id", "in", stale_prod.mapped("product_tmpl_id").ids),
    ])
    stale_bom.unlink()
    stale_prod.mapped("product_tmpl_id").unlink()

    # --- Create products ---
    chassis = Product.create({
        "name": "Bench Chassis Z",
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    frame = Product.create({
        "name": "Bench Frame Panel",
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    bolt = Product.create({
        "name": "Bench Bolt Pack",
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })

    # --- Create BoM: 1 Chassis = 2 Frames + 4 Bolt packs ---
    bom = BOM.create({
        "product_tmpl_id": chassis.product_tmpl_id.id,
        "product_qty": 1,
        "type": "normal",
        "consumption": "flexible",
    })
    BOMLine.create({
        "bom_id": bom.id,
        "product_id": frame.id,
        "product_qty": 2,
    })
    BOMLine.create({
        "bom_id": bom.id,
        "product_id": bolt.id,
        "product_qty": 4,
    })

    # --- Create and confirm MO for 10 units ---
    mo = MO.create({
        "name": "WH/MO/BENCH-PART-001",
        "product_id": chassis.id,
        "product_qty": 10,
        "bom_id": bom.id,
    })
    mo.action_confirm()
