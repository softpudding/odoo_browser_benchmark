# Cookbook notes — mrp_account MO close + Odoo 19 stock valuation

## `stock.valuation.layer` was removed in Odoo 19

Pre-19 code paths created `stock.valuation.layer` rows via
`stock_account`, which is what backlog prompts typically reference.
In Odoo 19 this model is gone. The replacement primitives live on
`stock.move` + a small new history model:

- `stock.move.value` (`fields.Monetary`) — per-move cash value,
  populated by `_set_value()` during `_action_done`.
- `stock.move.is_in` / `is_out` / `is_valued` / `is_dropship`
  (computed Booleans) — classify a done move for valuation.
- `product.value` (new model) — ring-buffer history of manual
  revaluations + move-level value recomputations.
- `stock.move.remaining_qty` / `remaining_value` — per-move
  FIFO remaining tail (the old SVL tail).

Check.py should filter by `production_id` (finished) vs
`raw_material_production_id` (raw) and assert `value>0` with
`is_in=True` / `is_out=True` respectively, NOT query an SVL table.

## `mrp_account._cal_price` only rolls cost into finished move for fifo/average

Source: `mrp_account/models/mrp_production.py::_cal_price`

```python
if finished_move.product_id.cost_method not in ('fifo', 'average'):
    finished_move.price_unit = finished_move.product_id.standard_price
    return True
# ... else: total_cost = sum(move.value for move in consumed_moves) + ...
# finished_move.price_unit = total_cost * (1 - byproduct_share) / quantity
```

With `cost_method='standard'` and the finished product's
`standard_price=0`, the hard-coded branch wins and the finished
`stock.move.value` ends up 0, even though component consumption
values are correctly computed. Tasks that seed `standard_price=0`
on the finished product to force "cost from rollup" MUST use
`property_cost_method='average'` (or `'fifo'`) on the category.

## `mrp_account._get_value_from_production` uses `stock.move.price_unit`

Source: `mrp_account/models/stock_move.py::_get_value_from_production`

```python
value = quantity * self.price_unit
```

So the `_set_value()` fallback path for the finished move
(`is_in=True` with `production_id`) reads `price_unit` that was
stamped by `_cal_price`, not `standard_price` directly. This is
how the rollup propagates into `move.value`.

## Location-level valuation_account_id is still required

Same trap as documented in `mrp_account.confirm_mo_check_account_move`:
even if the task only asserts on `stock.move.value` (not on
`account.move`), `_action_done` calls `_create_account_move()`
unconditionally on the move set, and its helper
`_should_create_account_move` crashes the transaction if the company
valuation accounts and the production-location /
internal-stock-location `valuation_account_id` fields are not set.
Seed must wire:

- `company.account_stock_valuation_id` → 140000 Stock Valuation
- `company.account_stock_journal_id` → any general journal
- Production location `valuation_account_id` → 500100 Cost of Production
- Internal Stock location `valuation_account_id` → Stock Valuation

## Single-click Produce All when qty_producing == product_qty + components on-hand

Components pre-loaded via
`stock.quant._update_available_quantity()` at the main WH stock
location, MO created via `MO.create() + action_confirm()`. Clicking
`button_mark_done` with `qty_producing` defaulting equal to
`product_qty` skips ALL wizards (no consumption wizard, no backorder
dialog). BU step count is tiny (≤9 steps) which is why this task
mis-calibrates toward "too easy" for hard-tier.

## `type='normal'` vs `'kit'` (`'phantom'`)

`mrp.bom.type` selection keys are `normal` and `phantom`. UI
labels are "Manufacture This Product" and "Kit" — do NOT seed
`type='kit'`.
