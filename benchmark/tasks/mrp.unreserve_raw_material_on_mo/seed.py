"""Seed for mrp.unreserve_raw_material_on_mo.

Category (MEDIUM): deep_ui_interaction — tests whether the agent can
locate the header **Unreserve** button on a confirmed+assigned MO and
release the reservation on its raw-material moves.

Pre-seeded entities:
  * Finished product 'Bench Unres Product' (consu/is_storable, tracking='none')
  * Component 'Bench Unres Mat' (consu/is_storable, tracking='none') with
    10 on-hand at WH/Stock.
  * Normal (non-phantom) BoM consuming 1 Bench Unres Mat per finished unit.
  * A CONFIRMED + RESERVED mrp.production 'MO-BENCH-UNRES' for 5 units.
    After action_confirm() + action_assign() the raw move is in state
    'assigned' with 5.0 reserved at WH/Stock.

The agent must open the MO and click the statusbar **Unreserve** button
(or the cog Actions → Unreserve server action). Post-state:
  - The raw move.state flips from 'assigned' → 'confirmed' (reservation
    released).
  - stock.quant.reserved_quantity on WH/Stock for Bench Unres Mat drops
    from 5.0 → 0.0.
  - mrp.production.reservation_state changes from 'assigned' → 'confirmed'.
  - MO.state remains 'confirmed' (Unreserve does NOT cancel or produce).

Seed invariants (asserted):
  - BoM is normal with 1 line.
  - MO state == 'confirmed' and reservation_state == 'assigned'.
  - move_raw_ids[0].state == 'assigned' with reserved quantity 5.0.
  - quant.reserved_quantity == 5.0 at WH/Stock for Bench Unres Mat.
"""

MO_NAME = "MO-BENCH-UNRES"
FINISHED = "Bench Unres Product"
COMPONENT = "Bench Unres Mat"
MO_QTY = 5.0
ON_HAND = 10.0

PRODUCT_NAMES = [FINISHED, COMPONENT]


def _cleanup(env):
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    Product = env["product.product"]

    stale_mo = MO.search([
        "|",
        ("name", "=", MO_NAME),
        ("name", "=like", MO_NAME + "-%"),
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
    MO = env["mrp.production"]

    # --- Storable products (tracking='none') ---
    finished = Product.create({
        "name": FINISHED,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })
    mat = Product.create({
        "name": COMPONENT,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
    })

    # --- Normal BoM: 1 finished = 1 component ---
    bom = BOM.create({
        "product_tmpl_id": finished.product_tmpl_id.id,
        "product_qty": 1,
        "type": "normal",
        "consumption": "flexible",
        "bom_line_ids": [
            (0, 0, {"product_id": mat.id, "product_qty": 1.0}),
        ],
    })

    # --- 10 component on-hand at WH/Stock (more than MO needs) ---
    warehouse = env["stock.warehouse"].search([
        ("company_id", "=", env.company.id),
    ], limit=1)
    stock_loc = warehouse.lot_stock_id
    env["stock.quant"]._update_available_quantity(mat, stock_loc, ON_HAND)

    # --- Confirmed MO for 5 units, then reserve ---
    mo = MO.create({
        "name": MO_NAME,
        "product_id": finished.id,
        "product_qty": MO_QTY,
        "bom_id": bom.id,
    })
    mo.action_confirm()
    mo.action_assign()

    # --- Sanity probes ---
    assert bom.type == "normal", "BoM must be normal"
    assert len(bom.bom_line_ids) == 1, "BoM must have exactly 1 line"
    assert mo.state == "confirmed", (
        f"MO state is {mo.state!r}, expected 'confirmed'"
    )
    assert len(mo.move_raw_ids) == 1, (
        f"Expected 1 raw move, found {len(mo.move_raw_ids)}"
    )
    raw_move = mo.move_raw_ids
    assert raw_move.product_id.id == mat.id, (
        f"Raw move must reference {COMPONENT}"
    )
    assert abs(raw_move.product_uom_qty - MO_QTY) < 1e-6, (
        f"Expected raw demand {MO_QTY}, got {raw_move.product_uom_qty}"
    )
    assert raw_move.state == "assigned", (
        f"Raw move state is {raw_move.state!r}, expected 'assigned' "
        f"(action_assign should have reserved 5 units of {ON_HAND} on-hand)"
    )
    assert mo.reservation_state == "assigned", (
        f"MO reservation_state is {mo.reservation_state!r}, expected 'assigned'"
    )

    # quant.reserved_quantity should equal 5.0 after action_assign
    quants = env["stock.quant"].search([
        ("product_id", "=", mat.id),
        ("location_id", "=", stock_loc.id),
    ])
    total_reserved = sum(quants.mapped("reserved_quantity"))
    assert abs(total_reserved - MO_QTY) < 1e-6, (
        f"Expected quant.reserved_quantity == {MO_QTY} after reservation, "
        f"got {total_reserved}"
    )

    # On-hand should still be 10 (reservation is a soft lock, not a move).
    total_on_hand = sum(quants.mapped("quantity"))
    assert abs(total_on_hand - ON_HAND) < 1e-6, (
        f"Expected {ON_HAND} {COMPONENT} on hand, got {total_on_hand}"
    )
