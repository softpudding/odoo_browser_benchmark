# Cookbook notes — mrp_account auto-journal on MO close

## stock_account `_should_create_account_move` requires a location-level valuation account

`stock_account/models/stock_move.py::_should_create_account_move` returns True only when ALL of:
1. `product.is_storable`
2. `stock.move.is_valued` (i.e. `is_in or is_out`)
3. `location_dest_id.valuation_account_id OR location_id.valuation_account_id`
4. `product.valuation == 'real_time'`

Base-snapshot `stock.location` records have `valuation_account_id = NULL` — condition (3) fails and no `account.move` is created even if the product category has `property_valuation='real_time'`. Seed must explicitly set `valuation_account_id` on:
- The Production location (`usage='production'`) — field labeled "Cost of Production" in the form.
- At least one internal Stock location — so the incoming/outgoing legs have a balanced counter-account.

```python
prod_loc = env["stock.location"].search([
    ("usage", "=", "production"),
    ("company_id", "=", env.company.id),
], limit=1)
prod_loc.valuation_account_id = cost_of_prod_account  # account_type='expense'

stock_loc = warehouse.lot_stock_id
stock_loc.valuation_account_id = env.company.account_stock_valuation_id
```

## mrp_account smart button on MO is labeled "WIP", NOT "Journal Entries"

`mrp_account/views/mrp_production_views.xml` adds a smart button `action_view_move_wip` showing `wip_move_count` under the label "WIP". It's only visible when the `mrp.account.wip.accounting` wizard has been run on the MO — which requires workorders with recorded times. Vanilla MO close (no workorders) leaves `wip_move_count=0` and the button stays hidden.

For tasks verifying the auto-generated `account.move`, the Journal Entries list at `/odoo/accounting/entries` is the canonical entry point — NOT a MO smart button.

## `stock.move.account_move_id` is Many2one (singular), NOT Many2many

`account_move_id = fields.Many2one('account.move', ...)`. Do not write `stock.move.account_move_ids` — that field doesn't exist and raises `AttributeError`. Each done stock.move links to at most one auto-generated posted entry.

## mrp_account is auto-installed

`mrp_account.__manifest__.auto_install=True` with deps `['mrp', 'stock_account']`. Both `mrp` (base_modules.txt) and `stock_account` (pulled in via sale/account) ship in the base snapshot, so `mrp_account` is already installed. Seed still calls `button_immediate_install()` defensively.

## MO close with qty_producing == product_qty skips the backorder dialog

With components on-hand (via `stock.quant._update_available_quantity`) and the MO created via `MO.create()` + `action_confirm()`, clicking "Produce All" (`button_mark_done`) closes the MO in a single click — no wizard, no backorder. This makes the BU step count low; it's a MEDIUM task because the cross-module navigation to Accounting is the main challenge, not the MO close itself.

## Inventory Valuation journal name in generic_coa

The auto-generated `account.move` lives in the "Inventory Valuation" journal (`account.journal.type='general'`, name="Inventory Valuation") with `name='STJ/YYYY/MM/####'`. BU identifies the entry correctly by journal name + Posted state + account lines (Stock Valuation debit, Cost of Production credit).
