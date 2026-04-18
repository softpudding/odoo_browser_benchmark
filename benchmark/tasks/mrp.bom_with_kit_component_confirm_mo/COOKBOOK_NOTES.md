# Cookbook notes — phantom/kit BoM auto-expansion and MO Reference trap

## `mrp.production.name` is NOT exposed as a Reference input on the draft form

The Odoo 19 `mrp.production_form_view` does not render an editable "Reference"
Char input in the form header. The visible `WH/MO/00001` string is the
auto-generated `name` (written by the `stock.picking.type` sequence at
`create()`). The ONLY paths to set a custom MO `name` are:

1. **Click the breadcrumb text in the top bar and overwrite the name** —
   only works in Odoo's web client where `<ControlPanel>` renders the
   record's `display_name` as an inline-editable Char. Fragile in
   Playwright, and browser-agents often don't recognize the breadcrumb
   as an editable input.
2. **JSON-RPC `create({'name': '...', ...})`** — what oracles should do.

On the Miscellaneous notebook tab there is a `origin` (Source) Char that
looks like a reference. Browser-use empirically typed `M-BENCH-KIT-001`
into **Source** — not the name — and its "I typed the reference" memory
log confused the two fields. This is a good calibration trap for hard
deep-UI-interaction tasks that need a deterministic `name` match in
`check.py`.

## `bom.explode()` walks phantom child BoMs on MO confirm

`mrp.production._get_moves_raw_values` calls `bom.explode(product,
factor, ...)` on the primary (non-phantom) BoM. Inside `explode`,
`_bom_find(bom_line.product_id, bom_type='phantom')` picks up kit BoMs
per line and recursively drills. The resulting `lines_done` skips all
lines whose `child_bom_id.type == 'phantom'` (they are replaced by
their leaves), so the `move_raw_ids` created on `action_confirm` only
reference atomic leaves.

Concretely, an MO for product P whose normal BoM is `[1x K, 1x F]`, where
K has a phantom BoM `[1x A, 2x B]` and F has no BoM, will produce
`move_raw_ids = [A=1, B=2, F=1]` — NOT `[K=1, F=1]`. The agent must
trust this expansion and NOT touch the Components tab.

## Kit expansion requires no stock — it happens at confirm

Phantom expansion is driven by `_bom_find(... bom_type='phantom')` which
only looks up BoMs by product. No stock availability, no routes, no
warehouse rules are involved. Seed only needs the phantom `mrp.bom`
record plus its `bom_line_ids`; no `stock.quant` required for expansion
itself (quants are only used for reservation, which happens after
confirm).

## Kit-type BoM: `mrp.bom.type = 'phantom'`

Odoo labels this in the BoM Type dropdown as "Kit". The underlying
selection value is `'phantom'` (the other option is `'normal'` →
"Manufacture This Product"). Do not write `type='kit'` — that's not a
valid selection key.

## Check `move_raw_ids` with `product_uom_qty`, not `quantity`

On a freshly-confirmed MO, `move.quantity` is 0.0 (nothing has been
done yet) while `move.product_uom_qty` carries the demanded amount.
The equivalent check for a DONE MO uses `move.quantity`. For a
confirmed-but-not-produced task, assert on `product_uom_qty`.
