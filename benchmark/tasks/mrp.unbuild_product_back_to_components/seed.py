"""Seed for mrp.unbuild_product_back_to_components.

Category (HARD): recovery_rollback.

Seeds:
  * Finished product 'Bench Assembly' (consu/is_storable, tracking='none')
  * Component 'Bench Screw' (consu/is_storable) — 3 per kit
  * Component 'Bench Housing' (consu/is_storable) — 1 per kit
  * A normal (non-phantom) BoM for Bench Assembly with 2 lines
  * 2 units of Bench Assembly on-hand at WH/Stock (via
    _update_available_quantity) so the Unbuild has stock to consume.

NO manufacturing order is pre-created — this is the "direct unbuild
without an MO" flow. The agent's unbuild will have `mo_id=False` and
will be driven purely by the BoM.

The agent must:
  1. Open Manufacturing > Products > Unbuild Orders (top-level menu).
  2. Click New to get an empty unbuild form.
  3. Set Product = Bench Assembly (BoM auto-fills from the only BoM).
  4. Set Quantity = 2.
  5. Leave Source Location = WH/Stock and Destination Location =
     WH/Stock at their defaults.
  6. Click Unbuild (statusbar button `action_validate` /
     `action_unbuild`).

Post-state:
  * mrp.unbuild with mo_id=False, product_id=Bench Assembly,
    product_qty=2.0, state='done'
  * stock.quant deltas: -2 Bench Assembly, +6 Bench Screw,
    +2 Bench Housing (all at WH/Stock).
"""

FINISHED = "Bench Assembly"
SCREW = "Bench Screw"
HOUSING = "Bench Housing"

PRODUCT_NAMES = [FINISHED, SCREW, HOUSING]


def _cleanup(env):
    Unbuild = env["mrp.unbuild"]
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    Product = env["product.product"]

    # mrp.unbuild in 'done' state cannot be unlinked cleanly — skip.
    stale_unbuild = Unbuild.search([
        ("product_id.name", "=", FINISHED),
    ])
    for u in stale_unbuild:
        if u.state == "draft":
            try:
                u.unlink()
            except Exception:
                pass

    # Any stray MOs for these products.
    stale_mo = MO.search([
        ("product_id.name", "in", PRODUCT_NAMES),
    ])
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
        ("name", "in", PRODUCT_NAMES),
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

    # --- Storable products (tracking='none') ---
    finished = Product.create({
        "name": FINISHED,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    screw = Product.create({
        "name": SCREW,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    housing = Product.create({
        "name": HOUSING,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })

    # --- Normal (non-phantom) BoM ---
    bom = BOM.create({
        "product_tmpl_id": finished.product_tmpl_id.id,
        "product_qty": 1,
        "type": "normal",
        "consumption": "flexible",
        "bom_line_ids": [
            (0, 0, {"product_id": screw.id, "product_qty": 3.0}),
            (0, 0, {"product_id": housing.id, "product_qty": 1.0}),
        ],
    })

    # --- 2 units of the finished product on-hand at WH/Stock ---
    warehouse = env["stock.warehouse"].search([
        ("company_id", "=", env.company.id),
    ], limit=1)
    stock_loc = warehouse.lot_stock_id
    env["stock.quant"]._update_available_quantity(finished, stock_loc, 2.0)

    # --- Sanity probes ---
    assert bom.type == "normal", "BoM must be normal (non-phantom)"
    assert len(bom.bom_line_ids) == 2, "BoM must have exactly 2 lines"

    # Verify on-hand qty is really 2 so the unbuild can consume it.
    on_hand = env["stock.quant"]._get_available_quantity(
        finished, stock_loc
    )
    assert abs(on_hand - 2.0) < 1e-6, (
        f"Expected 2.0 Bench Assembly on hand, got {on_hand}"
    )

    # No stray MOs exist for these products.
    assert not env["mrp.production"].search([
        ("product_id.name", "in", PRODUCT_NAMES),
    ]), "seed left stray MOs"
