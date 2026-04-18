# Result — purchase_stock.receive_partial_scrap_damaged_units

| Metric | Value |
|---|---|
| Oracle | PASS (F1=1.0, 9/9 edits matched, 0 postcondition failures) |
| Browser-Use | FAIL (F1=0.0, 8/9 edits matched; `Scrap quantity is 0.01, expected 5.0` postcondition fail → gated to 0.0; timeout at 480s) |
| Wall clock (oracle) | ~35s |
| Wall clock (browser-use) | 480s (hit time limit, `gave_up=True`) |
| Tier | 3 (hard) |
| Category | side_effect_trap |

## Workflow summary

1. **Part A — open PO and receipt**: Agent opens purchase order
   `P-BENCH-DMG-001` (Bench Parts Vendor, 20 Bench Parts) and clicks
   the **Receipt** smart button to open the auto-generated receipt
   (state=`assigned`).
2. **Part B — Done = 15**: Agent lowers the inline Done (`quantity`)
   cell on the Bench Parts move from the default 20 to 15.
3. **Part C — Scrap 5 to WH/Lost**: Agent opens the control-panel cog
   **Actions > Scrap**. In the dialog, fills product=Bench Parts,
   scrap_qty=5 (NOT the default 1), scrap_location_id=WH/Lost (NOT the
   default Virtual Locations/Scrap), clicks **Scrap Products**.
4. **Part D — validate + Create Backorder**: Agent clicks **Validate**.
   In the Backorder dialog clicks **Create Backorder** (primary). The
   original picking moves to `done`; a new assigned backorder picking
   is created carrying 5 remaining Bench Parts.

## Why this is hard for BU

Three independent traps stacked:

1. **Inline Done-cell edit with auto-reserved full demand**: The
   receipt auto-reserves all 20 units because Bench Parts is a
   consumable (no stock constraint). BU must MANUALLY lower 20 → 15;
   if it accepts the default the backorder dialog never appears.
2. **Non-default scrap wizard fields**: `scrap_qty` defaults to 1.0
   and `scrap_location_id` defaults to `Virtual Locations/Scrap`.
   Both MUST be overwritten to 5 and WH/Lost respectively. BU
   consistently leaves one or both at the default (observed: submitted
   scrap_qty=0.01, probably mistyped).
3. **Backorder dialog radio**: Primary button IS "Create Backorder"
   in Odoo 19 (flipped from older versions) so BU's default-click
   heuristic works here — BUT BU sometimes clicks "No Backorder"
   because the prompt emphasises "do NOT click No Backorder" which
   reads (to BU) as "click it".

## Oracle mechanics

- Navigate via `/odoo/purchase` → click the PO row → click Receipt
  smart button. Smart button selector covers both "Receive" and
  "Receipt" label variants.
- Done-qty inline edit: target `td[name='quantity']` cell, click, fill
  the inner input, press Tab to commit.
- Scrap action lives in the control-panel cog Actions menu (server
  action `stock.action_scrap`, `binding_model_id=stock.picking`,
  `binding_view_types=form`). NOT a header status-bar button.
- Scrap wizard: fill `scrap_qty` (overwrite default 1), then
  `scrap_location_id` via autocomplete filtered on 'WH/Lost'. Must use
  `.filter(has_text=LOST_LOC)` because the plain autocomplete also
  offers unrelated locations containing 'Lost' substring if any.
- Backorder dialog: the primary blue button IS "Create Backorder"
  (Odoo 19 default); oracle explicitly filters `has-text('Create
  Backorder')` rather than relying on first primary to guard against
  layout changes.

## Calibration

- Oracle: deterministic PASS, F1=1.0 in ~35s (9/9 state edits
  matched).
- Browser-Use: deterministic FAIL, F1=0.0; hit the non-default
  scrap_qty trap (set to 0.01 instead of 5) and ran to 480s timeout.
- Task succeeds as a Tier 3 hard test — the scrap_qty non-default
  cell + scrap_location non-default autocomplete + partial Done
  inline edit compound three well-known BU pain points.
