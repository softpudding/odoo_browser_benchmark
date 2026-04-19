# Cookbook notes from sale.edit_existing_quotation_add_optional_product

## `click_add_a_line` is the correct helper for "Add a product"

Unlike `sale.add_section_note_line_to_quotation` (which needs to hit
the non-default "Add a section" / "Add a note" controls), this task
targets the default/leftmost footer link. `oracle_helpers.click_add_a_line`
already prefers the link whose text contains "product":

```python
product_link = add_link.filter(has_text="product")
if product_link.count() > 0:
    product_link.first.click()
else:
    add_link.first.click()
```

So the helper does the right thing out of the box — no need for a
custom `_click_footer_control("Add a product")`. This is the single
biggest difference in oracle structure between the two tasks.

## Row index for the new line is 1, not 0

After `click_add_a_line`, the existing seeded row (Bench Existing Item)
remains at row index 0 and the new empty editable row is appended at
row index 1. Do NOT pass `row_index=0` to `set_o2m_many2one` or you
will overwrite the existing product — that's exactly the "edit
existing line instead of appending" trap the task is designed to
measure.

```python
click_add_a_line(page)                                          # appends row 1
set_o2m_many2one(page, 1, "product_template_id", PRODUCT_EXTRA)
set_o2m_field(page, 1, "product_uom_qty", "4")
```

## `product_template_id` not `product_id` (sol_o2m widget)

Per `create_quotation_with_customer_pricelist` cookbook: the Order
Lines sub-list view uses the `sol_o2m` widget, whose inline cell name
for the product column is `product_template_id`, NOT `product_id`.
`set_o2m_many2one(page, 1, "product_id", ...)` times out waiting for a
missing cell.

## Setting the product triggers an onchange that defaults qty=1

After the product is picked, the form fires an onchange that sets the
new line's `product_uom_qty` to 1.0 and `price_unit` to the product's
`list_price` (15.0 here). The qty must then be overwritten with 4 via
`set_o2m_field`. The Tab-commit is load-bearing: without it the row
stays in edit mode and a subsequent `save_form` can fire before the
onchange/write completes.

## state_spec match_key=[product_id] works here because we never see two lines with the same product

Entity-key is just `["Bench Extra Item"]`. The seed's existing line
uses a different product (`Bench Existing Item`), so there is no
collision. If the task is ever cloned to "add a second line for the
same product with a different qty", the match_key must be widened
(e.g. add `sequence` or `id`).

## `order_id` on sale.order.line normalizes to the SO name in the state diff

`sale.order.line.order_id` normalizes to the parent `sale.order.name`
(here `BENCH-ADD-LINE`), same as in `sale.add_section_note_line_to_quotation`.

## `product_uom_qty` normalizes to a JSON number

`sale.order.line.product_uom_qty` is a Float. `expected_state.json`
must use the JSON number `4.0` (or `4`), NOT the string `"4"`, because
the state-diff engine normalizes Float fields to Python floats (same
cookbook rule as `sale.order.line.discount` in
`sale.apply_discount_percent_on_sale_order_line`).

## No group-gating needed

Unlike the Disc.% column (gated by `sale.group_discount_per_so_line`),
the product column is always visible on the base `sale.order` form.
No `user_ids` group write is needed in the seed.
