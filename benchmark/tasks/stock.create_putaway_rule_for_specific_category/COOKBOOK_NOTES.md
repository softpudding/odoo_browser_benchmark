# Cookbook notes — stock.create_putaway_rule_for_specific_category

## stock.putaway.rule editable list: Product vs Product Category mutual-readonly

The Odoo 19 Putaway Rules list (`stock_putaway_list`) is `editable="bottom"`
and exposes BOTH `product_id` and `category_id` columns side-by-side. The view
defines reciprocal `readonly` attrs:

```xml
<field name="product_id"  readonly="... or category_id" .../>
<field name="category_id" readonly="... or product_id"  .../>
```

Implications for benchmark task design:

- "Pick category vs product" is **NOT** a hard pattern in this view. As soon as
  the agent fills one cell, the other is greyed out — visually unambiguous.
  Browser-use solves it on first try (F1=1.0).
- To make a putaway-rule task genuinely hard, you need to combine with:
  - Storage Category cell that becomes required when `sublocation == 'closest_location'`
    (a Selection field — non-default value)
  - Multi-row creation (several rules in one save)
  - A non-default `sublocation = 'closest_location'` choice

## Hard-tier calibration miss for `stock.create_putaway_rule_for_specific_category`

Tagged `hard` but BU passed F1=1.0. The product-vs-category radio-like split
is too visually obvious in the inline list. Future builders: if the *only*
non-default choice is "use the second m2o instead of the first", expect
BU to solve it.

## state_spec match_key with optional Many2ones

`stock.putaway.rule.match_key = [product_id, category_id, location_in_id]`
correctly emits `entity_key` of `[null, "Bench Cold Items", "WH/Stock"]` when
product_id is empty but category_id is set. The diff engine normalizes
unset Many2ones to JSON `null` (matching the existing pattern documented in
ODOO19_PATTERNS.md).
