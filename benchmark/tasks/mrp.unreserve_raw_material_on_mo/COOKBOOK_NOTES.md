# Odoo 19 quirks for mrp.unreserve_raw_material_on_mo

## `mrp.production.do_unreserve` cascades to BOTH raw AND finished moves

```python
# addons/mrp/models/mrp_production.py:2376-2377
def do_unreserve(self):
    (self.move_finished_ids | self.move_raw_ids).filtered(
        lambda x: x.state not in ('done', 'cancel')
    )._do_unreserve()
```

Both the raw component move **and** the finished-product move flip
state `assigned → confirmed` when the Unreserve button is clicked.
`expected_state.json` must list two `stock.move` set-edits (one per
move), not one. First oracle run that expected only the raw-move edit
gave Precision=0.667 with an unexpected-extra for the finished move.

## state_spec fields must include match_key fields

`benchmark/eval.py::read_state` only reads fields declared in
`spec['fields']`. Match_key fields are **not** auto-included. If
`raw_material_production_id` is in `match_key` but not `fields`, every
stock.move record lands at `entity_key=[null, null]` and the diff
engine falls back to `#dupN` suffixes (e.g. `[null, null]` +
`[null, null, "#dup1"]`). Fix: duplicate match_key fields into
`fields` so they're captured during `read_state`.

## `unreserve_visible` computed gate

```python
# addons/mrp/models/mrp_production.py:690-696
def _compute_unreserve_visible(self):
    for order in self:
        already_reserved = (
            order.state not in ('done', 'cancel')
            and order.mapped('move_raw_ids.move_line_ids')
        )
        any_quantity_done = any(order.move_raw_ids.mapped('picked'))
        order.unreserve_visible = not any_quantity_done and already_reserved
```

All three must be true for the header **Unreserve** button to appear:
1. MO state is `confirmed` / `progress` / `to_close` (not done / cancel).
2. At least one raw move has `move_line_ids` (i.e. reservation lines exist).
3. No raw move has `picked=True` (nothing already consumed).

A fresh `action_confirm()` + `action_assign()` satisfies all three on
a BoM with at least one raw line that has enough on-hand.

## `action_confirm()` alone does NOT reserve

Manufacturing pickings use `reservation_method='manual'` by default —
seeds must call `mo.action_assign()` explicitly after `mo.action_confirm()`
or `move_line_ids` stays empty (so `unreserve_visible=False` and the
button never renders). The mirror button **Check availability**
(`reserve_visible=True`) shows instead.

## `quant.reserved_quantity` vs `quantity`

Reservation is a soft lock:
- `quant.reserved_quantity = 5.0` after `action_assign()` on a 5-qty MO.
- `quant.quantity = 10.0` stays unchanged (on-hand is not deducted).
- `_get_available_quantity(product, loc)` returns 5 = 10 - 5 reserved.
- After `do_unreserve()`: `reserved_quantity = 0.0`, `quantity = 10.0`,
  `_get_available_quantity = 10.0`.

Seed sanity probes should use `sum(quants.mapped("reserved_quantity"))`
to verify the lock, not `_get_available_quantity` (the latter would
just return on-hand minus lock, which is ambiguous between "no lock
at all" and "lock released").

## `stock.move._do_unreserve` semantics

```python
# addons/stock/models/stock_move.py:927-953
def _do_unreserve(self):
    # ... filters out done/cancel/picked moves ...
    ml_to_unlink.unlink()
    (moves_to_unreserve - moves_not_to_recompute)._recompute_state()
```

Steps: (1) unlink `move_line_ids` that have `picked=False`; (2)
`_recompute_state()` computes fresh state from scratch. With 0
reserved lines and full remaining demand, state derives to
`'confirmed'` (not `'waiting'`, not `'draft'`, not `'assigned'`).

## Browser-use empirical behaviour (single shot, 97s)

BU solved this at F1=1.0 in 97.3s with no backtracks: it reads the
prompt's explicit "click the Unreserve button", navigates to the MO,
and clicks the labeled button in the statusbar. The task is a
straightforward **single-click capability check** — no wizard, no
modal, no non-default radios, no create-from-scratch. Use as a
calibration baseline for the MRP statusbar-button recognition pattern
when the button label unambiguously matches the prompt intent.

## Design trap: Cancel vs Unreserve

A naive agent might read "release the reservation" and click
**Cancel** (the red statusbar button). The prompt explicitly warns
against this. `check.py` also asserts `mo.state == 'confirmed'` post-
task and will fail with a clear error message ("is cancelled — the
task requires releasing the reservation, not cancelling the MO") if
an agent takes this path.
