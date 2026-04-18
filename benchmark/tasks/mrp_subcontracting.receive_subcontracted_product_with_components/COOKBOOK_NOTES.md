# Cookbook notes — mrp_subcontracting.receive_subcontracted_product_with_components

## Module prerequisites

`mrp_subcontracting` and the auto-install-but-dependency-gated
`mrp_subcontracting_purchase` bridge are NOT in `benchmark/base_modules.txt`.
Seed must `button_immediate_install` both:

```python
for name in ("mrp_subcontracting", "mrp_subcontracting_purchase"):
    mod = env["ir.module.module"].search([("name", "=", name)], limit=1)
    if mod and mod.state != "installed":
        mod.button_immediate_install()
```

## Phantom "Resupply Subcontractor" picking on PO confirm

`stock.warehouse.subcontracting_to_resupply` defaults to **True**. When a
subcontracting-type PO is confirmed, Odoo walks two parallel chains:

1. **Receipt**: incoming `stock.picking` (WH/IN/xxxxx) for the finished
   product from the subcontractor → this triggers `_action_confirm` on
   the subcontract move → auto-creates a `mrp.production` (subcontract
   type) linked via `move_orig_ids.production_id`.
2. **Resupply**: internal `stock.picking` (WH/RES/xxxxx) of type
   `subcontracting_resupply_type_id` that wants to move the BoM
   components from WH/Stock → Subcontracting location, even if the
   components are already at the subcontracting location (the
   procurement chain doesn't check target availability).

If the task **pre-stocks components at the subcontracting location**,
the resupply picking is spurious. Suppress it:

```python
warehouses = env["stock.warehouse"].search([])
warehouses.write({"subcontracting_to_resupply": False})
```

Leaving it on is fatal because:
- Both pickings share `origin == po.name`. Oracle `click_list_row(PO_NAME)`
  may click the resupply instead of the receipt.
- Validating the resupply with bypass-reservation moves components
  "from WH/Stock" even when WH/Stock had zero — committing a negative
  quant at WH/Stock that taints the components-backflush assertion.

## Subcontract BoM + subcontractor linkage

```python
bom = env["mrp.bom"].create({
    "product_tmpl_id": finished.product_tmpl_id.id,
    "product_qty": 1.0,
    "type": "subcontract",                             # NOT 'normal'
    "subcontractor_ids": [(6, 0, [subcontractor.id])], # REQUIRED for type='subcontract'
})
```

`mrp.bom._bom_subcontract_find` matches on `(product, picking_type,
company_id, bom_type='subcontract', subcontractor in subcontractor_ids)`
via `'parent_of'` — so the subcontractor can also be a child contact.

## Components pre-stock at subcontracting location

The subcontracting location is per-partner
(`partner.property_stock_subcontractor`) with a company fallback
(`env.company.subcontracting_location_id`):

```python
sub_loc = (subcontractor.with_company(env.company).property_stock_subcontractor
           or env.company.subcontracting_location_id)
env["stock.quant"]._update_available_quantity(part_a, sub_loc, 2.0)
env["stock.quant"]._update_available_quantity(part_b, sub_loc, 2.0)
```

Needs `stock.group_stock_multi_locations` on admin for the Subcontracting
location to render in the UI, and `stock.group_production_lot` for the
Detailed Operations popup to expose `lot_id` columns.

## Serial-tracked finished product causes subcontract MO splitting

With `tracking='serial'` on the finished product and `product_qty=2` on
the PO, the initially auto-created subcontract MO has `product_qty=2`.
On `picking.button_validate`, `_sync_subcontracting_productions` reads
the move_line lot→qty map and calls `_split_productions` — one MO per
lot — giving you **two done MOs** in the post-state where the seed only
had **one confirmed** MO.

`expected_state.json` encoding:

```json
{"model": "mrp.production",
 "entity_key": ["Bench Sub Assembly", "Bench Subcontractor Inc"],
 "field": "state", "op": "set", "norm_value": "done"},
{"model": "mrp.production",
 "entity_key": ["Bench Sub Assembly", "Bench Subcontractor Inc", "#dup1"],
 "field": "state", "op": "create", "norm_value": "done"}
```

Note the `#dup1` suffix the diff engine emits when two records share the
same `match_key` tuple — mandatory for the second MO's create diff.

## Receipt picking type needs lot-creation flags

For the Detailed Operations popup to expose an **autocomplete Create**
entry for brand-new serial names, the incoming picking type needs:

```python
picking_types = env["stock.picking.type"].search([("code", "=", "incoming")])
picking_types.write({"use_create_lots": True, "use_existing_lots": True})
```

Without `use_create_lots=True` the `lot_name` field is hidden; without
`use_existing_lots=True` the `lot_id` autocomplete is hidden. Both are
needed for the UI to let the agent type `BSA-2026-01` and select
`Create "BSA-2026-01"`.

## action_show_details on subcontract move opens a SPECIAL popup

`stock.move.action_show_details` for `is_subcontract=True` returns the
`mrp_subcontracting_view_stock_move_operations` view (inherits
`stock.view_stock_move_operations`, tweaks the move_line_ids context).
Selector for the Details button is unchanged:
`button[name='action_show_details']:visible` on the move row.

Inside the dialog, move_line rows have columns `product_id` (readonly),
`quantity`, `lot_id` (required because `tracking='serial'`). Autocomplete
Create option text is `Create "BSA-2026-01"` (with literal quotes).

## Canonical user flow

1. Open receipt → click move-row **Details** (not inline-edit).
2. In popup, ensure 2 move_line rows (auto-reserve may provide them; else **Add a line**).
3. For each row: click lot_id cell → type serial → click `Create "<serial>"`.
4. Set `quantity = 1` on each row (defaults to 0 for newly-added rows).
5. Save popup (`.modal-footer button.btn-primary:has-text('Save')`).
6. Click **Validate** on the picking form header.
7. Any follow-up backorder / confirmation dialog: accept primary.
