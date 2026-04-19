"""Seed for mrp.scrap_consumed_component_during_production.

Category: side_effect_trap (HARD).

Seeds:
  * Finished product 'Bench Assembly Kit' (storable, tracking='none')
  * Component 'Bench Screw' (storable, tracking='none') with 10 on-hand at
    WH/Stock (enough to cover the 3 screws per kit + the 1 scrapped unit)
  * A normal (non-phantom) BoM consuming 3 Bench Screw per kit, with no
    routing (no work orders)
  * A confirmed MO 'MO-BENCH-SCRAP' for 1 kit, reserved/assigned

The agent must:
  1. Open MO MO-BENCH-SCRAP.
  2. Open the form's cog/3-dots 'Actions' menu, click 'Scrap'.
  3. In the scrap wizard, set Product='Bench Screw', Quantity=1, keep
     defaults for the other fields.
  4. Validate the scrap.
  5. Click Produce All / Mark As Done on the MO header to finish the MO.
"""

MO_NAME = "MO-BENCH-SCRAP"
FINISHED = "Bench Assembly Kit"
COMPONENT = "Bench Screw"


def _cleanup(env):
    Scrap = env["stock.scrap"]
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    Product = env["product.product"]

    # Delete any draft scraps linked to a previous MO with this name.
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

    stale_prod = Product.with_context(active_test=False).search([
        ("name", "in", [FINISHED, COMPONENT]),
    ])
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


def setup(env):
    _cleanup(env)

    Product = env["product.product"]
    BOM = env["mrp.bom"]
    MO = env["mrp.production"]

    # --- Create products (tracking='none') ---
    finished = Product.create({
        "name": FINISHED,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    screw = Product.create({
        "name": COMPONENT,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })

    # --- BoM: 1 Bench Assembly Kit = 3 Bench Screw, no routing ---
    bom = BOM.create({
        "product_tmpl_id": finished.product_tmpl_id.id,
        "product_qty": 1,
        "type": "normal",
        "consumption": "flexible",
        "bom_line_ids": [
            (0, 0, {"product_id": screw.id, "product_qty": 3.0}),
        ],
    })

    # --- 10 on-hand screws at WH/Stock (3 consume + 1 scrap + buffer). ---
    warehouse = env["stock.warehouse"].search([
        ("company_id", "=", env.company.id),
    ], limit=1)
    stock_loc = warehouse.lot_stock_id
    env["stock.quant"]._update_available_quantity(screw, stock_loc, 10.0)

    # --- Confirmed MO for 1 kit ---
    mo = MO.create({
        "name": MO_NAME,
        "product_id": finished.id,
        "product_qty": 1,
        "bom_id": bom.id,
    })
    mo.action_confirm()
    try:
        mo.action_assign()
    except Exception:
        pass

    # --- Sanity checks (fail fast so seed problems surface early) ---
    assert bom.type == "normal", "BoM must be normal (non-phantom)"
    assert len(bom.bom_line_ids) == 1, "BoM must have exactly 1 line"
    assert mo.state == "confirmed", f"MO state is {mo.state!r}, expected 'confirmed'"
    # Only one raw move — 3 Bench Screw.
    assert len(mo.move_raw_ids) == 1, (
        f"Expected 1 raw move, found {len(mo.move_raw_ids)}"
    )
    assert abs(mo.move_raw_ids.product_uom_qty - 3.0) < 1e-6, (
        f"Expected raw qty 3.0, got {mo.move_raw_ids.product_uom_qty}"
    )
    assert mo.move_raw_ids.product_id.id == screw.id, (
        "Raw move must reference Bench Screw"
    )
