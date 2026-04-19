# mrp_account.mo_consume_and_close_check_valuation — Result

**Difficulty:** hard
**Tier:** 3
**Row:** 421
**time_limit_sec:** 480, **step_limit:** 300

## Oracle (PASS)
- wall_clock: 21.6s, steps: 0
- StateDiffF1: 1.0 (P=1.0, R=1.0)
- RequiredOpRecall: 1.0 (`mrp.production.button_mark_done`)
- HarmfulWriteRate: 0.0, StrictClean: True
- Observed=2 edits, matching=2, missing=0, extra=0

## Browser-use (PASS — calibration: task solvable, easier than hard target)
- wall_clock: 58.8s, ~9 steps
- StateDiffF1: 1.0 (P=1.0, R=1.0)
- RequiredOpRecall: 1.0
- HarmfulWriteRate: 0.0
- BU flow: login (admin/admin), navigate to /odoo/manufacturing, open
  MO-BENCH-VAL row, click Produce All (`button_mark_done`), done.

## Task design
Hard-tier cross-module valuation task: close a confirmed MO whose
finished product has `standard_price=0` on purpose so its stock.move
value must come from the component cost rollup (`_cal_price`). Checks
assert on Odoo 19 stock.move primitives (`value`, `is_in`, `is_out`,
`is_valued`) instead of the pre-19 `stock.valuation.layer` model.

## Key Odoo 19 pivots vs. original spec
1. `stock.valuation.layer` was removed in Odoo 19 — check.py uses
   `stock.move.value` + `is_in` / `is_out` / `is_valued` filtered by
   `production_id` (finished) and `raw_material_production_id` (raw
   components).
2. `_cal_price` is `cost_method`-gated: under `'standard'` it writes
   `product.standard_price` (0) to the finished move's `price_unit`.
   Seed uses `property_cost_method='average'` so the rollup fires.
3. Location `valuation_account_id` must be wired on both Production
   and Internal-Stock locations (same invariant as the medium
   `confirm_mo_check_account_move` task).

## Calibration
Browser-use succeeded in ~9 steps / 58.8s with F1=1.0 on the first
shot — below the hard-tier "<40% pass" target. Single-click Produce
All with pre-reserved components is not a genuine BU trap. Flagged in
STATUS.md calibration_note; escalation ideas documented there.
