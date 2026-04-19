# Cookbook notes — stock.receive_serial_tracked_product_two_serials

## `_action_assign` on a serial-tracked incoming move with demand ≥ 2 pre-creates N empty move_line rows

On a vanilla `stock.picking` whose move has `tracking='serial'` and
`product_uom_qty=2`, calling `action_confirm() + action_assign()` produces
**two** `stock.move.line` rows (not one qty=2 row), each with:

* `quantity = 0.0`
* `lot_id = False`
* `lot_name = False`
* `reserved_uom_qty = 1.0`

This materially reduces the difficulty of "enter two serials" tasks — the
agent does **not** need to click `Add a line` in the Detailed Operations
popup; they just tab into each pre-existing row's `lot_id` field and
create/pick a serial. If your task design requires forcing the `Add a
line` step (e.g., to trigger BU's row-creation failure mode), EITHER:

1. Seed `action_confirm()` only (skip `action_assign`) so the picking
   sits in `state=confirmed` with zero move_lines — the agent must
   click the header **Check Availability** button, which creates the N
   empty move_lines like `action_assign` would have;
2. OR, seed the picking with demand=1 (a single pre-reserved row) and
   ask the agent to split into two units — but that requires demand
   bumping and an explicit `Add a line` + qty decrement sequence.

The reference task `stock.cancel_picking_create_replacement_with_serial`
side-steps this by making the agent CREATE the picking from scratch
(Part B) — the freshly created picking before `action_confirm` has zero
move_lines, so the popup starts empty and the agent must add rows
manually. That's why THAT task is hard and this one calibrates easier.

## Receipts picking type: both `use_create_lots` + `use_existing_lots` required

For the Detailed Operations popup's `lot_id` autocomplete to show the
`Create "<text>"` option:

```python
picking_type.write({
    "use_create_lots": True,
    "use_existing_lots": True,
})
```

* `use_create_lots=True` alone → text-only `lot_name` input (no
  `stock.lot` row is ever created).
* `use_existing_lots=True` alone → `lot_id` m2o, but autocomplete
  dropdown omits the Create option.
* Both True → m2o with Create option. This is what check.py requires
  (`ml.lot_id.name == SN-XXX`).

## `stock.move.show_details_visible` on a serial-tracked move is auto-True

`stock.move._compute_show_details_visible` returns True when
`move.product_id.tracking != 'none'`. For this task, the serial-tracked
product trips that clause automatically — **no need to grant
`stock.group_stock_multi_locations` to admin** just for the Details
button to render. Granting `stock.group_production_lot` is still needed
so the popup's list view exposes the `lot_id` column itself (otherwise
the column is hidden and only the `quantity` cell renders).

## BU's typical path through the popup (single-shot PASS pattern)

Observed in the BU run for this task (16 steps total, 122s wall clock):

```
Step 1-6: navigate → login → /odoo/inventory → click Receipts tile
Step 7:   click row WH/IN/BENCH-SERIAL in the list
Step 8:   click the Details button on the Bench Serial Item move line
Step 9:   click td[name=lot_id] on row 1, type SN-BENCH-A001
Step 10:  click the combobox input, wait, retype, wait 2s
Step 11:  click the autocomplete "Create SN-BENCH-A001" option
Step 11b: click td[name=lot_id] on row 2, type SN-BENCH-A002
Step 13:  retarget via click on row 2 after misclick, type SN-BENCH-A002
Step 14:  click autocomplete "Create SN-BENCH-A002", click Save
Step 15:  back on picking, click Validate
Step 16:  done
```

The only friction was the first autocomplete open (step 9-10) requiring
a re-click + retype. Once BU learned the combobox pattern, the second
serial went through on step 13-14 without retry. To force BU to fail in
a future variant, design the task so the lot `create` option is gated
behind a non-autocomplete pathway (e.g., separate form open via
internal-link button) or so multiple near-identical serials must be
distinguished.

## Oracle's outer-form Save-before-Validate safety

In the oracle, after clicking the popup's primary Save button, a
defensive outer-form `.o_form_button_save` click is included before
`click_status_button(page, "Validate")`. This is a holdover from
observations on the reference task where the popup's Save occasionally
leaves the outer form in dirty state, and Validate would fire before
web_save lands. For THIS task it is a no-op because Odoo 19's popup
Save persists cleanly, but the defensive click is cheap and keeps the
oracle robust to future Odoo UI changes.
