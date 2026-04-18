"""Seed for mrp.scrap_component_during_partial_production.

Category: side_effect_trap (HARD).

Seeds:
  * 'Bench Widget' finished product + components 'ScrewA' and 'ScrewB'
  * A BoM consuming 5 ScrewA + 5 ScrewB per Bench Widget
  * A confirmed MO 'M-BENCH-SCRAP-001' for 5 units of Bench Widget
  * A scrap reason tag named 'Defective batch' (used in the wizard)
  * Enough on-hand stock of ScrewA and ScrewB at WH/Stock so the MO can
    be produced after the scrap.

The agent must:
  1. Open the MO form cog 'Actions' menu and click 'Scrap'.
  2. Fill the scrap wizard (ScrewA, qty=2, source=WH/Stock,
     reason='Defective batch').
  3. Validate the scrap.
  4. Produce All / Mark As Done to finish the MO.
"""

MO_NAME = "M-BENCH-SCRAP-001"
FINISHED = "Bench Widget"
COMP_A = "ScrewA"
COMP_B = "ScrewB"
REASON_TAG = "Defective batch"


def setup(env):
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    Product = env["product.product"]
    ReasonTag = env["stock.scrap.reason.tag"]
    Scrap = env["stock.scrap"]

    # --- Cleanup prior runs ---
    stale_scraps = Scrap.with_context(active_test=False).search([
        ("production_id.name", "=", MO_NAME),
    ])
    # Can't unlink a done scrap; best-effort delete draft ones and leave done
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
    stale_mo.unlink()

    stale_prod = Product.search([("name", "in", [FINISHED, COMP_A, COMP_B])])
    stale_bom = BOM.search([
        ("product_tmpl_id", "in", stale_prod.mapped("product_tmpl_id").ids),
    ])
    stale_bom.unlink()
    stale_prod.mapped("product_tmpl_id").unlink()

    # --- Scrap reason tag (leave existing one if present; create otherwise) ---
    tag = ReasonTag.search([("name", "=", REASON_TAG)], limit=1)
    if not tag:
        tag = ReasonTag.create({"name": REASON_TAG})

    # --- Create finished + components ---
    finished = Product.create({
        "name": FINISHED,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    screw_a = Product.create({
        "name": COMP_A,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    screw_b = Product.create({
        "name": COMP_B,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })

    # --- Create BoM: 1 Bench Widget = 5 ScrewA + 5 ScrewB ---
    bom = BOM.create({
        "product_tmpl_id": finished.product_tmpl_id.id,
        "product_qty": 1,
        "type": "normal",
        "consumption": "flexible",
        "bom_line_ids": [
            (0, 0, {"product_id": screw_a.id, "product_qty": 5}),
            (0, 0, {"product_id": screw_b.id, "product_qty": 5}),
        ],
    })

    # --- On-hand stock at WH/Stock (enough to both scrap & produce) ---
    wh = env["stock.warehouse"].search([
        ("company_id", "=", env.company.id),
    ], limit=1)
    stock_loc = wh.lot_stock_id
    # Need at least 25 ScrewA (5 per widget * 5 units + 2 scrap buffer = 27)
    env["stock.quant"]._update_available_quantity(screw_a, stock_loc, 40.0)
    env["stock.quant"]._update_available_quantity(screw_b, stock_loc, 40.0)

    # --- Create + confirm MO for 5 units ---
    mo = MO.create({
        "name": MO_NAME,
        "product_id": finished.id,
        "product_qty": 5,
        "bom_id": bom.id,
    })
    mo.action_confirm()
    # Reserve components so they're available when we scrap / produce.
    try:
        mo.action_assign()
    except Exception:
        pass
