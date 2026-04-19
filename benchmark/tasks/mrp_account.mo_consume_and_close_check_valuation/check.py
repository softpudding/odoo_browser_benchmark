"""Postcondition checks for mrp_account.mo_consume_and_close_check_valuation.

Validates (Odoo 19 stock valuation primitives — `stock.valuation.layer`
was replaced by `stock.move.value` + `product.value` in Odoo 19):

1. The MO MO-BENCH-VAL exists and is in 'done' state.
2. qty_produced == product_qty == 1.0 (no backorder was created).
3. Exactly one done finished `stock.move` is linked to the MO via
   `stock.move.production_id` (product = Bench Assembly), with
   `is_in=True`, `is_valued=True` and `value > 0`.
4. Exactly two done raw-component `stock.move` records are linked via
   `stock.move.raw_material_production_id` (products = Bench Component
   1 / 2), each with `is_out=True`, `is_valued=True`, `value > 0` and
   approximately equal to the seeded component standard cost (10.0).
5. The finished move's `value` approximately equals the sum of the
   two raw moves' `value` (cost rollup, ~= 20.0).
"""


MO_NAME = "MO-BENCH-VAL"
FINISHED_NAME = "Bench Assembly"
COMPONENT_NAMES = ["Bench Component 1", "Bench Component 2"]
COMPONENT_COST = 10.0
EXPECTED_FINISHED_VALUE = COMPONENT_COST * len(COMPONENT_NAMES)
TOL = 0.01


def check(env):
    failures = []

    mos = env["mrp.production"].search([("name", "=", MO_NAME)])
    if not mos:
        return [f"Manufacturing order {MO_NAME!r} not found"]
    if len(mos) > 1:
        failures.append(
            f"Expected exactly 1 MO named {MO_NAME!r}, found {len(mos)}"
        )
    mo = mos[0]

    # MO state.
    if mo.state != "done":
        failures.append(f"MO state is {mo.state!r}, expected 'done'")

    # Quantities.
    if abs(mo.product_qty - 1.0) > 1e-6:
        failures.append(
            f"MO product_qty is {mo.product_qty}, expected 1.0 (do not reduce)"
        )
    if abs(mo.qty_produced - 1.0) > 1e-6:
        failures.append(
            f"MO qty_produced is {mo.qty_produced}, expected 1.0"
        )

    # No backorder MO should exist.
    backorders = env["mrp.production"].search([
        ("name", "=like", MO_NAME + "-%"),
    ])
    if backorders:
        failures.append(
            f"Unexpected backorder MO(s) created: {backorders.mapped('name')}"
        )

    # Sanity check: the MO's finished product is the expected one.
    if mo.product_id.name != FINISHED_NAME:
        failures.append(
            f"MO product is {mo.product_id.name!r}, expected {FINISHED_NAME!r}"
        )

    StockMove = env["stock.move"]

    # --- Finished stock.move (production_id=MO, product=finished) ---
    fin_moves = StockMove.search([
        ("production_id", "=", mo.id),
        ("product_id", "=", mo.product_id.id),
        ("state", "=", "done"),
    ])
    if len(fin_moves) != 1:
        failures.append(
            f"Expected exactly 1 done finished stock.move for MO "
            f"{MO_NAME!r} (production_id + product={FINISHED_NAME!r}), "
            f"found {len(fin_moves)}"
        )
    finished_value = 0.0
    if fin_moves:
        fin = fin_moves[0]
        if not fin.is_in:
            failures.append(
                f"Finished stock.move is_in={fin.is_in!r}, expected True"
            )
        if not fin.is_valued:
            failures.append(
                f"Finished stock.move is_valued={fin.is_valued!r}, expected True"
            )
        if fin.value <= 0:
            failures.append(
                f"Finished stock.move value={fin.value!r}, expected > 0"
            )
        finished_value = fin.value

    # --- Raw stock.moves (raw_material_production_id=MO, 2 components) ---
    raw_moves = StockMove.search([
        ("raw_material_production_id", "=", mo.id),
        ("state", "=", "done"),
    ])
    if len(raw_moves) != 2:
        failures.append(
            f"Expected exactly 2 done raw stock.moves for MO "
            f"{MO_NAME!r} (raw_material_production_id), found {len(raw_moves)}: "
            f"{raw_moves.mapped('product_id.name')}"
        )

    raw_products = set(raw_moves.mapped("product_id.name"))
    missing_comps = [n for n in COMPONENT_NAMES if n not in raw_products]
    if missing_comps:
        failures.append(
            f"Raw moves missing component(s) {missing_comps!r} "
            f"(observed products: {sorted(raw_products)!r})"
        )

    total_raw_value = 0.0
    for rm in raw_moves:
        if not rm.is_out:
            failures.append(
                f"Raw stock.move for {rm.product_id.name!r} is_out="
                f"{rm.is_out!r}, expected True"
            )
        if not rm.is_valued:
            failures.append(
                f"Raw stock.move for {rm.product_id.name!r} is_valued="
                f"{rm.is_valued!r}, expected True"
            )
        if rm.value <= 0:
            failures.append(
                f"Raw stock.move for {rm.product_id.name!r} has value="
                f"{rm.value!r}, expected > 0 (consumption)"
            )
        if abs(rm.value - COMPONENT_COST) > TOL:
            failures.append(
                f"Raw stock.move for {rm.product_id.name!r} has value="
                f"{rm.value!r}, expected ~= {COMPONENT_COST!r}"
            )
        total_raw_value += rm.value

    # --- Cost rollup: finished value ~= sum of raw values ---
    if fin_moves and raw_moves:
        if abs(finished_value - total_raw_value) > TOL:
            failures.append(
                f"Finished move value {finished_value!r} does not match "
                f"sum of raw move values {total_raw_value!r}"
            )
        if abs(finished_value - EXPECTED_FINISHED_VALUE) > TOL:
            failures.append(
                f"Finished move value {finished_value!r} does not match "
                f"expected total {EXPECTED_FINISHED_VALUE!r}"
            )

    return failures
