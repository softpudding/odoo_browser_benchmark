# Cookbook notes — purchase_stock.receive_partial_scrap_damaged_units

## Scrap from `stock.picking` auto-creates a picking move

`stock.scrap._prepare_move_values()` sets `picking_id=self.picking_id.id`
on the generated `stock.move` (also `scrap_id=self.id`). Consequence:
after validating a scrap from a picking, `picking.move_ids` contains
BOTH the original receipt move AND the scrap move. Any `check.py` that
asserts `len(picking.move_ids)==1` will fail.

Filter pattern used here:

```python
moves = picking.move_ids.filtered(
    lambda m: m.product_id.id == product.id and not m.scrap_id
)
```

## `purchase.order.name` drives `stock.picking.origin`, NOT `purchase.order.origin`

When `po.button_confirm()` generates the receipt, Odoo stamps
`picking.origin = po.name` (the PO reference like `P00001`). Writing
`purchase.order.origin = "P-BENCH-DMG-001"` does NOT affect
`picking.origin`. To pin picking.origin deterministically for
state-diff entity keys, pin `purchase.order.name` in seed:

```python
po = env["purchase.order"].create({
    "name": "P-BENCH-DMG-001",      # <-- determines picking.origin
    "partner_id": vendor.id,
})
```

Same pattern noted in ODOO19_PATTERNS.md for `sale.order.name` →
`stock.picking.origin` on delivery pickings.

## Validate-with-backorder shrinks original move's demand to Done qty

When `picking.button_validate()` is called and the agent picks
**Create Backorder**, Odoo splits the moves via `_action_done()`:

- Original picking: `move.product_uom_qty` is REDUCED from the full
  demand (e.g. 20) to the actual Done amount (e.g. 15).
- Backorder picking: gets a fresh move with the remaining demand (5).

Do NOT assert `product_uom_qty == original_demand` on the done
picking — it will fail because Odoo has already rewritten it. Assert
`product_uom_qty == Done quantity` instead.

## `stock.scrap.scrap_location_id` + `location_id` need multi-locations group

Both `scrap_location_id` and `location_id` fields on
`stock.scrap.form_view2` are gated by
`groups="stock.group_stock_multi_locations"`. In base snapshots where
the admin doesn't have it, those fields are *invisible* and the agent
cannot change them (the wizard writes the default Virtual
Locations/Scrap silently). Seed must:

```python
admin.group_ids |= env.ref("stock.group_stock_multi_locations")
```

## `WH/Lost` (or any named inventory location) must be seeded

Odoo only ships "Virtual Locations/Scrap" (created per-company by
`_create_scrap_location`). A user-named "Lost" sub-location under the
main warehouse (so `complete_name == "WH/Lost"`) requires:

```python
wh = env["stock.warehouse"].search([("company_id", "=", env.company.id)], limit=1)
env["stock.location"].create({
    "name": "Lost",
    "usage": "inventory",               # any inventory-usage loc is a scrap dest
    "location_id": wh.view_location_id.id,
    "company_id": env.company.id,
})
```

Verify the final `complete_name` resolves to exactly `WH/Lost` (no
extra whitespace / different parent) before relying on it in
`expected_state.json` entity keys or `check.py` location comparisons.

## Scrap on a consumable picking bypasses the Insufficient-Qty wizard

`stock.scrap.check_available_qty()` short-circuits when
`product_id.is_storable == False`. For a task that scraps from a
pre-validate picking (source = Vendors), using
`type='consu', is_storable=False` avoids the secondary
`stock.warn.insufficient.qty.scrap` wizard that would otherwise
intercept the Validate click. If you need a storable product,
you'd have to pre-seed on-hand qty at the picking's `location_id`
(which is the Vendors supplier location — not a normal stock quant
source) or accept the secondary wizard as an extra step for the
agent.

## Backorder-id normalizes to the parent picking's display_name

With `state_spec.match_key: [origin, partner_id, backorder_id]` on
`stock.picking`, the backorder entity_key's third slot is the display
name of the original picking (e.g. `"R-BENCH-DMG-001"`). Pin the
original's `picking.name` in seed so this is deterministic:

```python
for picking in po.picking_ids:
    picking.write({"name": "R-BENCH-DMG-001"})
```

Otherwise the sequence-generated name (e.g. `WH/IN/00001`) changes
every run → expected_state.json entity_key never matches.

## Partial-Done + Create-Backorder dialog primary is "Create Backorder"

Consistent with the ODOO19_PATTERNS.md note: the blue primary button
in the backorder confirmation dialog IS "Create Backorder" in Odoo
19 (swapped from older versions where "No Backorder" was primary).
Oracle selectors should explicitly filter `has-text('Create
Backorder')` to be robust.
