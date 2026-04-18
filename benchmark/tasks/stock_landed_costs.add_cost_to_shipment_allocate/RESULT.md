# Result — stock_landed_costs.add_cost_to_shipment_allocate

| Metric | Value |
|---|---|
| Oracle | PASS (F1=1.0, 8/8 edits matched, 0 postcondition failures) |
| Browser-Use | PASS (F1=1.0, 8/8 edits matched, 0 postcondition failures, 183.2s wall clock) |
| Wall clock (oracle) | ~28s |
| Wall clock (browser-use) | 183.2s single-shot |
| Tier | 3 (hard) |
| Category | policy_trap |

## Workflow summary

1. **Part A — open Landed Costs new form**: Agent navigates to
   Inventory > Operations > Landed Costs (`/odoo/landed-costs`) and
   clicks the list-view **New** button to open a blank form.
2. **Part B — pick completed receipt**: Agent types `R-BENCH-LC-001`
   in the **Transfers** many2many_tags input and selects the match
   from the autocomplete. Two distractor validated receipts
   (`R-BENCH-LC-DISTRACTOR-A/B`) share the `R-BENCH-LC` prefix, so
   loose prefix typing yields multiple candidates.
3. **Part C — add Freight cost line**: Agent clicks **Add a line**
   under Additional Costs, fills `Freight` in the product autocomplete,
   leaves `Split Method = By Quantity` (seeded as the Freight template's
   default via `split_method_landed_cost='by_quantity'`), and sets
   `Cost = 45`.
4. **Part D — Compute + Validate**: Agent clicks the in-form **Compute**
   button below the cost-lines subtotal (generating the valuation
   adjustment line 15/unit × 3 units = 45 EUR), THEN clicks the
   header **Validate** button to move the record to state `done`.

## Why this is designed as hard

Three compound traps intended for BU:

1. **Two-button action split (Compute + Validate)**: Clicking Validate
   on a cost with no `valuation_adjustment_lines` populated raises
   `"Cost and adjustments lines do not match. You should maybe
   recompute the landed costs."` from `_check_sum`. The agent MUST
   click Compute first to materialise the adjustment lines.
2. **picking_ids many2many_tags autocomplete**: The Transfers field
   is gated by domain
   `[('company_id', '=', company_id), '|',
   ('move_ids.is_in', '!=', False), ('move_ids.is_out', '!=', False)]`
   — only validated pickings appear. The two distractor receipts are
   also `done`, so the typed prefix `R-BENCH-LC` returns 3 options;
   the agent must pick R-BENCH-LC-001.
3. **Seeded non-default split_method**: `Freight.split_method_landed_cost`
   is `by_quantity`, which is NOT the first enum value (`equal`).
   When the agent picks `Freight`, the `onchange_product_id` hook
   stamps `by_quantity` onto the cost line automatically; the trap
   is that a defensive agent might "fix" the split method back to
   `Equal` and break the per-unit 15 EUR allocation.

Empirically, browser-use single-shot solved the task in 183s with
F1=1.0 — the prompt is verbose enough (explicit Compute before
Validate instruction, exact Cost value, exact picking name) that BU
executed both clicks in order. The task remains useful as a positive
reference point and stresses the complete `stock.landed.cost` form
flow (m2m_tags domain filter + inline cost_lines + valuation
adjustment diff + two-phase button chain).

## Oracle mechanics

- URL is `/odoo/landed-costs` (from
  `stock_landed_costs.action_stock_landed_cost.path`). Menu path:
  Inventory > Operations > Adjustments > Landed Costs.
- **Transfers** picker: click the input inside
  `.o_field_widget[name='picking_ids']`, type `R-BENCH-LC-001`, pick
  the autocomplete entry via `.filter(has_text='R-BENCH-LC-001')`.
- **Add a line**: `.o_field_widget[name='cost_lines']
  .o_field_x2many_list_row_add a`. Product + Cost edits happen on
  the newly-added `.o_data_row.o_selected_row` row.
- **Compute**: `button[name='compute_landed_cost']` lives in the
  subtotal footer of the Additional Costs tab, NOT the header. Do
  NOT use `button.o_form_button_create` selectors — that is the
  top-bar "New" button and will create a phantom draft record.
- **Validate**: `.o_statusbar_buttons button[name='button_validate']`
  in the header statusbar. Save the form first (if dirty) because
  Validate on an unsaved form is a no-op in Odoo 19's Owl form
  controller.

## Calibration

- Oracle: deterministic PASS, F1=1.0 in ~28s.
- Browser-Use (single-shot): PASS, F1=1.0 in 183s. The 45 EUR
  cost + single-move-allocation math is small enough that BU does
  not get confused by the Compute/Validate ordering when the
  prompt is explicit about both buttons. This task is a useful
  positive-case cookbook entry for the `stock.landed.cost` form.
