# Odoo 19 quirks for mrp.confirm_mo_produce_partial_keep_backorder

## `mrp.production._split_productions` renames the original MO on backorder

When `qty_producing < product_qty` and the agent clicks **Create
backorder** on the `mrp.production.backorder` wizard, Odoo's
`_split_productions` runs the following on the ORIGINAL MO:

1. `backorder_sequence` flips from `0` → `1`.
2. `name` is rewritten via `_get_name_backorder`:
   - `"MO-BENCH-PARTIAL"` → `"MO-BENCH-PARTIAL-001"` (suffix added
     because the existing name has no trailing `-\d+`).
3. `product_qty` is rewritten from `10.0` → `4.0` (the actually-
   produced qty), matching the split-move demand.
4. `state` flips to `done`, `qty_produced=4.0`.

The backorder record is born with `backorder_sequence=2` and
`name="MO-BENCH-PARTIAL-002"`. Consequence for state_spec/check.py:

- **Use `name` as match_key, not `id` or `procurement_group_id`**. The
  diff engine sees the rename as `delete(MO-BENCH-PARTIAL)` +
  `create(MO-BENCH-PARTIAL-001)` — 5 delete edits + 5 create edits.
  That's intentional and the expected_state.json must enumerate
  BOTH sides.
- `check.py` must look up the original as `MO-BENCH-PARTIAL-001`,
  NOT `MO-BENCH-PARTIAL` (which no longer exists post-task).
- The prompt must warn the user about the rename, or they'll
  assume "MO-BENCH-PARTIAL still exists" and manually verify the
  wrong name.

## `show_produce` vs `show_produce_all` — the button label flips

```
show_produce_all = state_ok and qty_producing in (0, product_qty)
show_produce     = state_ok and qty_producing not in (0, product_qty)
```

- Default view (qty_producing == product_qty): label = **"Produce All"**.
- After qty_producing edit to < product_qty: label = **"Produce"**.

Both buttons have `name="button_mark_done"`. The oracle must click the
`button_mark_done` that's currently visible (filtered by label if both
are rendered in the DOM across flex layouts).

## `qty_producing` is inline-editable on the form header

No popover / no wizard — it's a Char input on the main form next to
Quantity. The widget appears in `.o_field_widget[name='qty_producing']
input`. **Tab out of the field after editing** to trigger the
`_compute_show_produce` recompute (otherwise the wrong header button
stays visible).

## Backorder wizard: primary button = "Create backorder" (action_backorder)

```
<button name="action_backorder"  string="Create backorder" class="btn-primary"/>
<button name="action_close_mo"   string="No Backorder"     class="btn-secondary"/>
```

The primary (blue) button is the CORRECT choice for a partial-
production task that wants to keep the remaining qty as a sibling MO.
Unlike the stock.picking backorder flow (where "No Backorder" is
sometimes the correct non-default), here "Create backorder" matches
the intent — so the task is effectively a calibration check (BU
consistently clicks the primary and passes).

## `_update_available_quantity` on a confirmed-and-assigned MO

If the seed does `action_confirm()` + `action_assign()` and then tries
to assert `_get_available_quantity(mat, stock_loc) == 10`, the probe
returns **0** because `_get_available_quantity` subtracts reserved qty.
Use the raw quant sum instead:

```python
total = sum(env["stock.quant"].search([
    ("product_id", "=", mat.id),
    ("location_id", "=", stock_loc.id),
]).mapped("quantity"))
```

## Browser-use empirical behavior (single shot, 88s)

BU passes this task readily: it reads the prompt's explicit "change
left-hand 10.00 to 4", finds the Quantity Producing input, types 4,
clicks Produce, then clicks the primary Create backorder button. F1=1.0.
Task serves as **calibration baseline** for the backorder-dialog
pattern when the primary-button choice is also the correct one. To
make it genuinely hard-tier, invert the dialog choice (make "No
Backorder" the correct answer, e.g. "close the MO and discard the
remaining 6 units").
