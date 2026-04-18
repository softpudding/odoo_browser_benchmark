# Odoo 19 quirks for mrp.scrap_component_during_partial_production

## stock.scrap "reason" is a many2many tag, not a Char

In Odoo 19 the scrap wizard uses `scrap_reason_tag_ids`
(`stock.scrap.reason.tag`, many2many). There is **no** Char `reason`
field. Tasks that ask the agent to enter a "reason" must:

1. Seed a `stock.scrap.reason.tag` (e.g. `{"name": "Defective batch"}`)
   in the seed (Odoo ships none by default).
2. Phrase the prompt as "add the existing tag X" so the agent picks the
   tag from the autocomplete instead of trying to type a free-text note.

`check.py` validates with `s.scrap_reason_tag_ids.mapped("name")`
membership, never `s.reason`.

## "Scrap" button on the MO is in the cog Actions menu

`mrp.action_production_order_scrap` is an `ir.actions.server` with
`binding_model_id=mrp.production` and `binding_view_types="form"`. It is
NOT a header status-bar button. Agents (and oracles) must:

```python
page.locator(".o_cp_action_menus button:visible, "
             ".o_control_panel .fa-cog:visible").first.click()
page.locator(".dropdown-menu:visible .dropdown-item:has-text('Scrap')").first.click()
```

This is exactly the kind of "non-default action menu" pattern that
defeats browser-use — it tends to look only at the visible header
buttons (Produce All / Mark As Done / Check Availability / Unreserve) and
never opens the cog menu.

## stock.scrap state-diff entity_key is the linked production_id

When `stock.scrap` is tracked with `match_key: [production_id]`, the
diff engine emits **two** "create" rows for the production link itself:
one with `field=production_id, norm_value=<MO name>` and the rest of
the fields. Don't forget to include the `production_id` row in
`expected_state.json`, otherwise observed=6 vs expected=5 → strict FAIL.

## stock.scrap.scrap_qty default is 1.0

The wizard pre-fills `scrap_qty=1`. Browser-use almost always submits
the default and never edits the cell, even when the prompt says
"quantity 2". Good failure pattern for hard-tier tasks: ask for any
quantity != 1.

## `do_scrap` requires available stock at source location

`stock.scrap.action_validate` calls `check_available_qty()` which
opens an "Insufficient Quantity To Scrap" wizard
(`stock.warn.insufficient.qty.scrap`) if the source location is empty.
Seed must set `stock.quant._update_available_quantity(...)` for every
component the agent might scrap. Setting more than the BoM consumption
+ the scrap quantity also avoids the secondary consumption-warning
wizard during Produce All.
