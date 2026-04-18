# Cookbook notes — stock.cancel_picking_create_replacement_with_serial

## stock.picking header Confirm button is labelled "Mark as Todo"

`addons/stock/views/stock_picking_views.xml` (line 117):

```xml
<button name="action_confirm" invisible="state != 'draft'"
        string="Mark as Todo" type="object" class="oe_highlight"
        groups="base.group_user" data-hotkey="q"/>
```

So `click_status_button(page, "Confirm")` will time out on a receipt
form in Odoo 19. Use `"Mark as Todo"` instead (or fall back across both
labels for older bases). Prompt copy should also say **Mark as Todo**
or the dual-label form to avoid BU confusion.

## stock.picking move_ids list add-label is "Add a Product"

The Operations tab `move_ids` list has `add-label="Add a Product"` (not
the generic "Add a line"). Oracles that look for the Add-a-line text
will never find it. Select both labels to be safe:

```python
".o_form_view .o_list_renderer a:has-text('Add a Product'):visible, "
".o_form_view .o_list_renderer a:has-text('Add a line'):visible"
```

## Receipts list URL path

`action_picking_tree_incoming` defines `path="receipts"`, so the stable
URL is `/odoo/inventory/receipts` (mirror of `/odoo/inventory/deliveries`
for outgoing). Prefer this over navigating to `/odoo/inventory` and
clicking the Receipts kanban tile — the kanban card's click target is
ambiguous (wrapping `<a>` vs the per-count button) and sometimes lands
on an action that filters to `Ready` only, hiding cancelled records.

## stock.move.show_details_visible gate in draft

`stock.move._compute_show_details_visible` returns `False` when
`move.state == 'draft'`. That means the **Details** button on a move
line does NOT render until the picking is Confirmed
(action_confirm → state in {`confirmed`, `assigned`}). An oracle that
tries to open Detailed Operations before Confirming will time out —
the button is literally absent. Task design: Part B (create+confirm)
must come before Part C (fill serials in popup).

## Detailed Operations popup appends phantom empty rows

In the `stock.view_stock_move_line_operation_tree` list (editable="bottom"
multi_edit=1), tabbing out of the last cell of the last row auto-appends
a new empty row. For serial receipt tasks that expect exactly N
move_lines, the oracle must sweep after filling and delete any rows
whose lot_name is empty (e.g. via `.o_list_record_remove` trash icon).
Leaving the phantom row triggers a validation error at Validate time:

```
Invalid Operation: You need to supply a lot/serial number for product:
- <product name>
```

## stock.picking.partner_id entity_key normalization on new records

`state_spec.yaml` with `match_key: [origin, partner_id]` on `stock.picking`
produces entity_keys of `[null, "<Partner Name>"]` for a picking created
during the task (origin is left null by default). Encode this in
`expected_state.json` as:

```json
{"entity_key": [null, "Bench Supplier Inc"], "op": "create", ...}
```

The first slot really is JSON `null`, not the picking's auto-assigned
name (e.g. "WH/IN/00003") — diff engine normalizes `origin=False` to
`null` before emitting entity_key.

## Demand vs Quantity decouple on serial receipts

On a serial-tracked receipt line with demand=0 but move_line quantity
sums to N>0, Odoo 19's `button_validate` still succeeds (the move
autocomputes `product_uom_qty=0` displayed, but the transfer is done
based on move_lines). So a "filling demand" check in `check.py`
(`product_uom_qty == expected`) is a useful *additional* gate that
catches BU's pattern of forgetting the Demand cell when creating the
new receipt — separate from the serial-count postcondition. Without
this, a partially-correct BU run can pass the strict clause while the
original task intent (demand=2) is lost.
