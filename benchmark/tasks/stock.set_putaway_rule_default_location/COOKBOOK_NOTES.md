# Cookbook notes — stock.set_putaway_rule_default_location

## Calibration confirmation: product-level putaway-rule creation is NOT hard

This row corroborates the earlier finding documented for
`stock.create_putaway_rule_for_specific_category` — a plain editable-bottom
list with three m2o fields (location_in / product / location_out) is a
solid medium/tier-2 pattern but does NOT trap BU. BU completed the
workflow single-shot at F1=1.0 in 91.7s (vs. 34.6s oracle baseline).

Key signals:

- The Configuration submenu path (Inventory → Configuration → Putaway
  Rules) is plainly labelled; BU navigated via the top-menu without
  getting sidetracked by the product form's putaway smart button.
- The Product / Product Category mutual-readonly cells make the
  product-level choice visually obvious once Product is filled — BU
  never even glanced at the Category column.
- Saving an editable-bottom list row is reliable via `.o_list_button_save`
  or Tab-out of the last cell; no "save swallowed" issues like the
  Details popup pattern on stock.move.

## Seed recipe: product-level putaway rule task

Reusable pattern for future putaway tasks:

```python
admin = env.ref("base.user_admin")
admin.group_ids |= env.ref("stock.group_stock_multi_locations")
# Optional but documented in the task spec — pairs naturally with
# multi-locations for any warehouse routing scenario.
admin.group_ids |= env.ref("stock.group_adv_location")

# Sublocation
shelf = env["stock.location"].create({
    "name": "Shelf B",
    "location_id": stock_loc.id,  # the WH/Stock internal view
    "usage": "internal",
})

# Storable product
tmpl = env["product.template"].create({
    "name": "Bench Putaway Item",
    "type": "consu",
    "is_storable": True,
    ...
})
```

No pre-existing putaway rule; the agent creates it from scratch via the
Configuration menu.

## state_spec + expected_state for product-level putaway rules

`stock.putaway.rule.match_key = [product_id, category_id, location_in_id]`
normalises a product-level rule's entity_key to
`["Bench Putaway Item", null, "WH/Stock"]` — category_id is the empty m2o
position (null), same convention as category-level rules where product_id
is null. Include `category_id` in the expected_state so the diff engine
sees a `create` edit setting it to `null` (otherwise F1 can drop to 0.75
from "Unexpected extra edits").

## When to escalate to tier 3

Same ladder as the category-rule task:

- Require a non-default `sublocation='closest_location'` Selection value
  (makes the Storage Category cell required, adding a fourth m2o).
- Multi-row creation (e.g. "add two putaway rules in one save") — the
  editable-bottom row loses `o_selected_row` between saves, so the agent
  must re-click New and keep both rows straight.
- Combine with a non-trivial Package Type m2m_tags selection (gated by
  `stock.group_tracking_lot`).
