# Cookbook notes — stock_landed_costs.add_cost_to_shipment_allocate

## `stock_landed_costs` is not in the base snapshot — install on demand

The module is NOT listed in `benchmark/base_modules.txt`. Seed must
install it before doing anything else:

```python
mod = env["ir.module.module"].search(
    [("name", "=", "stock_landed_costs")], limit=1
)
if mod and mod.state != "installed":
    mod.button_immediate_install()
```

Guard downstream seed ops with `if "stock.landed.cost" not in env.registry`
so a partial install doesn't crash the whole setup.

## `stock.landed.cost.picking_ids` domain requires validated pickings

The Transfers m2m_tags widget on the landed-cost form filters via:

```xml
domain="[('company_id', '=', company_id), '|',
  ('move_ids.is_in', '!=', False),
  ('move_ids.is_out', '!=', False)]"
```

`stock.move.is_in` / `is_out` are stored Booleans (from `stock_account`)
that flip to True only when `move.state == 'done'` AND the move is a
net incoming/outgoing move. Implication: seed MUST validate the
receipt picking before the landed-cost form will accept it in the
autocomplete. Leaving the receipt in `assigned` silently yields an
empty dropdown.

```python
for mv in picking.move_ids:
    mv.write({"quantity": qty, "picked": True})
picking.with_context(skip_backorder=True).button_validate()
```

## `cost_method` must be FIFO or AVCO, NOT standard

`stock.landed.cost.get_valuation_lines` skips moves whose
`product.cost_method` is not `'fifo'` or `'average'`. With the default
company cost method `'standard'`, Compute silently produces zero
valuation adjustments and Validate fails with "Cost and adjustments
lines do not match."

Seed a dedicated product category with the right method:

```python
cat = env["product.category"].create({
    "name": "Bench LC Category",
    "property_cost_method": "fifo",
    "property_valuation": "periodic",  # avoid accounting journal setup
    "parent_id": env.ref("product.product_category_goods").id,
})
```

`property_valuation='periodic'` is the cheap path — it keeps
`move.value` update working at validate time WITHOUT requiring the
company to have stock journal / stock valuation / price diff
accounts configured. `real_time` requires each of those three
accounts on the category or the validate call crashes looking up
`accounts.get('stock_valuation')`.

## `product.template.landed_cost_ok` is `invisible` unless `type='service'`

The field only renders on the product form when `type='service'`. It
is writable via JSON-RPC regardless, but for a task that wants the
agent to toggle "Is a Landed Cost" in the UI, the product MUST be a
service. The Freight product here is `type='service'` with
`landed_cost_ok=True` and `split_method_landed_cost='by_quantity'`
— all pre-seeded so the agent only does the landed-cost workflow.

## Compute is a footer button inside the Additional Costs tab

The **Compute** button is NOT in the form header statusbar. It's
rendered as a class-`float-end btn-secondary` inside the
`oe_subtotal_footer` group below the cost_lines editable list:

```xml
<button colspan="2" name="compute_landed_cost" string="Compute"
        type="object" class="float-end btn-secondary"
        invisible="state != 'draft'"/>
```

Oracles / agents targeting "Validate" by `.o_statusbar_buttons
button` skip Compute entirely and hit the
`Cost and adjustments lines do not match` UserError.

## Validate requires the record to be saved first

Form's `.o_statusbar_buttons button[name='button_validate']` is a
server-action button that operates on `self` — it needs a persisted
record. In Owl, clicking it on a dirty new form discards the click.
Oracles must click `.o_form_button_save` (if visible) BEFORE
triggering Validate. Same trap burns agents that call Validate
from an unsaved create form.

## Do NOT use `button.o_form_button_create` as a Validate selector

`.o_form_button_create` is the top-bar "New" button (the little
plus icon beside the breadcrumb), NOT a generic primary action.
If you include it in a fallback OR-selector for Validate, Playwright
will click "New" on the saved record, creating a second draft
`stock.landed.cost` with amount_total=0. This leaves a phantom row
in after_state and poisons the state diff.

Correct selector:

```python
page.locator(".o_statusbar_buttons button[name='button_validate']:visible")
```

## `valuation_adjustment_lines` is regenerated on every Compute

`stock.landed.cost.compute_landed_cost()` starts with:

```python
AdjustementLines.search([('cost_id', 'in', self.ids)]).unlink()
```

So clicking Compute twice (or editing cost_lines.price_unit between
computes) is safe — each call rebuilds the adjustment lines from the
current cost_lines + targeted pickings.

## `split_method` is persisted per cost line, inherited from product template

`stock.landed.cost.lines.onchange_product_id` stamps
`line.split_method = product.product_tmpl_id.split_method_landed_cost
or line.split_method or 'equal'`. If the Freight product has a
non-default `split_method_landed_cost`, the agent gets the "right"
split for free on product pick. Don't rely on this as the sole hard-
pattern — a savvy agent can overwrite it. For a task that FORCES a
specific allocation, pre-seed the product's default AND assert
`cl.split_method == 'by_quantity'` in check.py.

## Many2many_tags `picking_ids` autocomplete + distractor pickings

Typing a short prefix (`R-BENCH-LC`) in the Transfers autocomplete
returns all validated receipts whose name starts with that prefix.
Two seeded distractor receipts share the prefix to discourage
loose autocomplete. Oracles / agents must type the exact
`R-BENCH-LC-001` and use
`.filter(has_text='R-BENCH-LC-001')` on the dropdown items. Loose
substring match (no filter) picks the wrong row and writes a
`picking_ids` referencing a distractor — Compute then allocates
against the wrong product and the valuation-adjustment-line diff
fails.
