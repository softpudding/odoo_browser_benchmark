# Result — stock.cancel_picking_create_replacement_with_serial

| Metric | Value |
|---|---|
| Oracle | PASS (F1=1.0, 8/8 edits matched, 0 postcondition failures) |
| Browser-Use | FAIL (F1=0.0, 8/8 state edits matched BUT `Replacement demand for Bench Serial Widget is 0.0, expected 2.0` postcondition fail → F1 gated to 0.0) |
| Wall clock (oracle) | ~60s |
| Wall clock (browser-use) | ~249s |
| Tier | 3 (hard) |
| Category | recovery_rollback |

## Workflow summary

1. **Part A — cancel original**: Agent opens receipt `R-BENCH-CANCEL-001`
   (state=assigned, Bench Supplier Inc, Bench Hardware Item qty=5) and
   clicks the header **Cancel** button. Picking state → `cancel`.
2. **Part B — new receipt**: Agent creates a fresh receipt for Bench
   Supplier Inc, adds one line for `Bench Serial Widget` with demand 2,
   clicks **Mark as Todo** (Odoo 19's Confirm label on receipts).
3. **Part C — two serials in Detailed Operations**: Agent opens the
   **Details** popup on the move line. Because tracking=`serial` and
   demand=2, `action_assign` auto-generates 2 empty move_lines; the agent
   fills each with a unique lot_name (`BS-001`, `BS-002`) and quantity 1
   via the lot_name autocomplete `Create` option.
4. **Part D — validate**: Agent clicks **Validate**. No backorder dialog
   appears (qty matches demand). Picking state → `done`.

## Why this is hard for BU

Two independent failure modes:

1. **Skipping the Cancel**: BU often reads the task as "create a new
   receipt" and forgets Part A entirely. Check.py asserts original is
   `state='cancel'`.
2. **Only-first-serial trap**: BU enters `BS-001` on the first
   move_line and tries to validate with a single line of qty=2. Odoo
   raises `You need to supply a lot/serial number for product: Bench
   Serial Widget` because serials require exactly one move_line per unit.
3. **Demand field left blank**: BU often fills the product but forgets
   `Demand=2`; Odoo will still let you Validate (move_lines drive the
   real qty) but the postcondition on `product_uom_qty == 2.0` flags it.
   This was the observed BU failure mode in calibration.

## Oracle mechanics

- Navigate directly to `/odoo/inventory/receipts` (path defined on
  `action_picking_tree_incoming`). The Inventory kanban dashboard's card
  click is too fragile.
- Use `Mark as Todo` header label for the action_confirm button
  (Odoo 19 changed wording; "Confirm" label is not on the receipt form).
- Fill the move_ids `Add a Product` link (label is **Add a Product**,
  not the generic "Add a line").
- In Detailed Operations: after filling row 2's qty and pressing Tab,
  editable-bottom lists can append a phantom third empty row — the
  oracle walks the rows after filling, deletes any without a serial.
- Backorder: omitted — demand=2 and qty=1+1=2 match exactly.

## Calibration

- Oracle: deterministic PASS, F1=1.0 in ~60s.
- Browser-Use: FAIL (F1=0.0), hard via demand-field-blank trap.
- Task succeeds as a Tier 3 hard test. Gate postcondition (demand==2)
  catches BU's typical "ignore demand field, just validate" pattern.
