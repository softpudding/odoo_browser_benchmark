"""Seed for mrp.scrap_component_during_production.

Category: side_effect_trap (HARD).

Seeds:
  * 'Bench Final Product' (manufacture) + two stockable components
    'Bench Component A' and 'Bench Component B' (the distractor).
  * A BoM consuming 5 units of each component per 1 Bench Final Product.
  * Enough on-hand stock at WH/Stock of both components.
  * A confirmed, in-progress MO 'M-BENCH-PROD-001' for 5 units of
    Bench Final Product, with qty_producing=5 already set (i.e. the
    operator has picked up the order) but NOT yet marked as done.

The agent must:
  1. Open the MO form cog 'Actions' menu and click 'Scrap'.
  2. Fill the scrap wizard (product=Bench Component A, quantity=2).
  3. Validate the scrap.
  4. Produce All / Mark As Done to finish the MO.
"""

MO_NAME = "M-BENCH-PROD-001"
FINISHED = "Bench Final Product"
COMP_A = "Bench Component A"
COMP_B = "Bench Component B"


def setup(env):
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    Product = env["product.product"]
    Scrap = env["stock.scrap"]

    # --- Cleanup prior runs ---------------------------------------------
    stale_scraps = Scrap.with_context(active_test=False).search([
        ("production_id.name", "=", MO_NAME),
    ])
    for s in stale_scraps:
        if s.state == "draft":
            try:
                s.unlink()
            except Exception:
                pass

    stale_mo = MO.search([("name", "=", MO_NAME)])
    for mo in stale_mo:
        if mo.state not in ("draft", "cancel"):
            try:
                mo.action_cancel()
            except Exception:
                pass
    try:
        stale_mo.unlink()
    except Exception:
        pass

    stale_prod = Product.search([("name", "in", [FINISHED, COMP_A, COMP_B])])
    if stale_prod:
        stale_bom = BOM.search([
            ("product_tmpl_id", "in", stale_prod.mapped("product_tmpl_id").ids),
        ])
        try:
            stale_bom.unlink()
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
    comp_a = Product.create({
        "name": COMP_A,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    comp_b = Product.create({
        "name": COMP_B,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })

    # --- BoM: 1 Bench Final Product = 5 A + 5 B -------------------------
    bom = BOM.create({
        "product_tmpl_id": finished.product_tmpl_id.id,
        "product_qty": 1,
        "type": "normal",
        "consumption": "flexible",
        "bom_line_ids": [
            (0, 0, {"product_id": comp_a.id, "product_qty": 5}),
            (0, 0, {"product_id": comp_b.id, "product_qty": 5}),
        ],
    })

    # --- On-hand stock --------------------------------------------------
    wh = env["stock.warehouse"].search([
        ("company_id", "=", env.company.id),
    ], limit=1)
    stock_loc = wh.lot_stock_id
    # Need at least 25 of each component for 5 Bench Final Product; add
    # a buffer so the 2 scrapped ones can also be taken from stock.
    env["stock.quant"]._update_available_quantity(comp_a, stock_loc, 50.0)
    env["stock.quant"]._update_available_quantity(comp_b, stock_loc, 50.0)

    # --- Create + confirm MO, put it 'in progress' ----------------------
    mo = MO.create({
        "name": MO_NAME,
        "product_id": finished.id,
        "product_qty": 5,
        "bom_id": bom.id,
    })
    mo.action_confirm()
    try:
        mo._action_assign()
    except Exception:
        try:
            mo.action_assign()
        except Exception:
            pass
    # Mark the order as in-progress by setting qty_producing. This is
    # what clicking 'Produce' on the form does. We intentionally do NOT
    # call button_mark_done so the MO stays open for the agent to
    # finish after scrapping.
    try:
        mo.write({"qty_producing": 5.0})
    except Exception:
        pass
