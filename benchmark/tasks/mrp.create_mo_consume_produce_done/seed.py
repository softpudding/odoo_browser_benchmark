"""Seed for mrp.create_mo_consume_produce_done.

Category: closed_loop_cross_module (HARD).

Seeds:
  * 'Bench Assembly' (finished) plus two stockable components
    'Bench Part A' and 'Bench Part B'.
  * A BoM (type=normal, product_qty=1) consuming 1 Bench Part A and
    2 Bench Part B per 1 Bench Assembly.
  * Enough on-hand stock at WH/Stock of each component for the run.
  * NO pre-existing manufacturing order — the agent must create one.

The agent must:
  1. Create a new MO for 3 units of Bench Assembly from scratch.
  2. Click Confirm.
  3. Click Produce All / Mark as Done and accept the consumption
     dialog so the MO closes with qty_produced=3.
"""

FINISHED = "Bench Assembly"
PART_A = "Bench Part A"
PART_B = "Bench Part B"


def setup(env):
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    BOMLine = env["mrp.bom.line"]
    Product = env["product.product"]

    # --- Cleanup prior runs ---------------------------------------------
    # Any stale MO for the finished product or its prior versions.
    stale_prod = Product.with_context(active_test=False).search([
        ("name", "in", [FINISHED, PART_A, PART_B]),
    ])
    if stale_prod:
        stale_mos = MO.search([
            ("product_id", "in", stale_prod.ids),
        ])
        for mo in stale_mos:
            if mo.state not in ("draft", "cancel"):
                try:
                    mo.action_cancel()
                except Exception:
                    pass
        try:
            stale_mos.unlink()
        except Exception:
            pass

        stale_boms = BOM.search([
            ("product_tmpl_id", "in", stale_prod.mapped("product_tmpl_id").ids),
        ])
        try:
            stale_boms.unlink()
        except Exception:
            pass
        try:
            stale_prod.mapped("product_tmpl_id").unlink()
        except Exception:
            pass

    # --- Create finished + components -----------------------------------
    finished = Product.create({
        "name": FINISHED,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    part_a = Product.create({
        "name": PART_A,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    part_b = Product.create({
        "name": PART_B,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })

    # --- BoM: 1 Bench Assembly = 1 Part A + 2 Part B --------------------
    bom = BOM.create({
        "product_tmpl_id": finished.product_tmpl_id.id,
        "product_qty": 1,
        "type": "normal",
        "consumption": "flexible",
    })
    BOMLine.create({
        "bom_id": bom.id,
        "product_id": part_a.id,
        "product_qty": 1,
    })
    BOMLine.create({
        "bom_id": bom.id,
        "product_id": part_b.id,
        "product_qty": 2,
    })

    # --- On-hand stock for components -----------------------------------
    wh = env["stock.warehouse"].search([
        ("company_id", "=", env.company.id),
    ], limit=1)
    stock_loc = wh.lot_stock_id
    # Need 3 Part A and 6 Part B; add a buffer.
    env["stock.quant"]._update_available_quantity(part_a, stock_loc, 20.0)
    env["stock.quant"]._update_available_quantity(part_b, stock_loc, 40.0)

    # NO MO is created — the agent must build it from scratch.
