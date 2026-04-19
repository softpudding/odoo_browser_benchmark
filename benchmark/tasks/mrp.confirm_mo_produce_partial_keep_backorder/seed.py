"""Seed for mrp.confirm_mo_produce_partial_keep_backorder.

Category (HARD): policy_trap.

Seeds:
  * Finished product 'Bench Widget' (storable, tracking='none')
  * Component 'Bench Mat' (storable, tracking='none') with 10 on-hand at
    WH/Stock (exactly enough for 10 widgets; no scrap buffer needed).
  * A normal (non-phantom) BoM consuming 1 Bench Mat per Bench Widget
  * A CONFIRMED mrp.production 'MO-BENCH-PARTIAL' for 10 units of
    Bench Widget (state='confirmed', reserved/assigned).

The agent must:
  1. Open MO MO-BENCH-PARTIAL.
  2. Set Quantity Producing = 4 (down from the default 10).
  3. Click Produce (not Produce All, since qty_producing < product_qty).
  4. On the 'Create Backorder' dialog, click the PRIMARY 'Create
     backorder' button (NOT 'No Backorder').

Post-state:
  * Original MO MO-BENCH-PARTIAL has state='done', qty_producing=4.0,
    product_qty=4.0 (Odoo's _split_productions rewrites product_qty on
    the original to the actually-produced qty).
  * A sibling MO MO-BENCH-PARTIAL-001 (backorder_sequence=2) exists
    with state in {'confirmed','to_close','progress'} and
    product_qty=6.0, sharing procurement_group_id with the original.
"""

MO_NAME = "MO-BENCH-PARTIAL"
FINISHED = "Bench Widget"
COMPONENT = "Bench Mat"
MO_QTY = 10.0

PRODUCT_NAMES = [FINISHED, COMPONENT]


def _cleanup(env):
    MO = env["mrp.production"]
    BOM = env["mrp.bom"]
    Product = env["product.product"]

    # Cancel+unlink original MO and ANY backorder (name starts with
    # MO-BENCH-PARTIAL and may have a -NNN suffix).
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

    # --- Normal (non-phantom) BoM: 1 Bench Widget = 1 Bench Mat ---
    bom = BOM.create({
        "product_tmpl_id": finished.product_tmpl_id.id,
        "product_qty": 1,
        "type": "normal",
        "consumption": "flexible",
        "bom_line_ids": [
            (0, 0, {"product_id": mat.id, "product_qty": 1.0}),
        ],
    })

    # --- 10 Bench Mat on-hand at WH/Stock ---
    warehouse = env["stock.warehouse"].search([
        ("company_id", "=", env.company.id),
    ], limit=1)
    stock_loc = warehouse.lot_stock_id
    env["stock.quant"]._update_available_quantity(mat, stock_loc, 10.0)

    # --- Confirmed MO for 10 units ---
    mo = MO.create({
        "name": MO_NAME,
        "product_id": finished.id,
        "product_qty": MO_QTY,
        "bom_id": bom.id,
    })
    mo.action_confirm()
    try:
        mo.action_assign()
    except Exception:
        pass

    # --- Sanity probes ---
    assert bom.type == "normal", "BoM must be normal (non-phantom)"
    assert len(bom.bom_line_ids) == 1, "BoM must have exactly 1 line"
    assert mo.state == "confirmed", (
        f"MO state is {mo.state!r}, expected 'confirmed'"
    )
    assert abs(mo.product_qty - MO_QTY) < 1e-6, (
        f"MO product_qty is {mo.product_qty}, expected {MO_QTY}"
    )
    # qty_producing defaults to product_qty for an assigned MO on the
    # form, and is 0 under the hood until the form computes _set_qty_producing.
    # No need to pre-seed it.
    assert len(mo.move_raw_ids) == 1, (
        f"Expected 1 raw move, found {len(mo.move_raw_ids)}"
    )
    assert abs(mo.move_raw_ids.product_uom_qty - MO_QTY) < 1e-6, (
        f"Expected raw demand {MO_QTY}, got {mo.move_raw_ids.product_uom_qty}"
    )
    assert mo.move_raw_ids.product_id.id == mat.id, (
        f"Raw move must reference {COMPONENT}"
    )
    # Total quant on-hand at WH/Stock for Bench Mat should be 10.0
    # (regardless of whether it's reserved on the MO's raw moves). Use the
    # raw quants field, not `_get_available_quantity` (that one subtracts
    # reserved qty).
    total_on_hand = sum(env["stock.quant"].search([
        ("product_id", "=", mat.id),
        ("location_id", "=", stock_loc.id),
    ]).mapped("quantity"))
    assert abs(total_on_hand - 10.0) < 1e-6, (
        f"Expected 10 {COMPONENT} on hand, got {total_on_hand}"
    )
