# Cookbook notes from sale.apply_discount_percent_on_sale_order_line

## `sale.group_discount_per_so_line` gates Disc.% column visibility

The per-line Disc.% column on `sale.order.line` is declared with
`optional="show"` / `groups="sale.group_discount_per_so_line"` in the
Order Lines sub-list view (see `sale.sale_order_form`). In Odoo 19 this
group is NOT granted to admin by default on the benchmark base snapshot
— opening any SO form will render the o2m list without the Disc.%
column, even for `admin`, until the group is added.

Seed-time mitigation: grant the group to both admin AND user_root (any
ORM compute that touches the `field.groups` check runs under
SUPERUSER_ID for internal writes):

```python
discount_group = env.ref("sale.group_discount_per_so_line",
                         raise_if_not_found=False)
admin = env.ref("base.user_admin")
root = env.ref("base.user_root")
if discount_group:
    discount_group.sudo().write({
        "user_ids": [(4, admin.id), (4, root.id)],
    })
```

Without this, the oracle's `set_o2m_field(page, 0, "discount", "10.0")`
times out waiting for a `td[name='discount']` cell that the view never
rendered.

## Inline cell edit: `set_o2m_field` is the canonical path

For inline edits of a specific column in an editable one2many list
(like Disc.%), `benchmark/oracle_helpers.set_o2m_field(page, row_index,
field_name, value)` is the reliable recipe:

1. Locate `.o_form_view .o_list_renderer .o_data_row` at `row_index`.
2. Click the `td[name='discount']` cell to enter edit mode.
3. Clear the input with `fill("")`.
4. Type the value.
5. Press Tab to commit.
6. Wait for `_wait_no_loading`.

The Tab commit is load-bearing: without it, the row stays in edit mode
and the subsequent `save_form` sometimes fires before the onchange /
write happens, producing a silent no-op.

## Do NOT trust row order — resolve row by product name

Although the seed creates line A then line B (so line A is at row 0),
relying on `row_index=0` is fragile if Odoo ever reorders lines on the
fly (e.g. because of a section insertion elsewhere in the view). The
defensive pattern is to scan all `.o_data_row` nodes for the product
name and return the matching index:

```python
def _row_index_for_product(page, product_name):
    rows = page.locator(".o_form_view .o_list_renderer .o_data_row")
    for i in range(rows.count()):
        if product_name in rows.nth(i).inner_text():
            return i
    return 0
```

This also catches bugs where the seed produces lines in the wrong
order, because the oracle will still target the right row rather than
silently writing the discount to the wrong line.

## `discount` on `sale.order.line` is a float, not a Char

`sale.order.line.discount` is `fields.Float(digits='Discount')` with a
`_inverse` that clamps to [0, 100]. Both `"10"` and `"10.0"` are
accepted by the UI input (the Float widget parses via `parse_float`);
the stored value after commit is always `10.0`. `expected_state.json`
must use `"norm_value": 10.0` (JSON number), not `"10.0"` (string),
because the state-diff engine normalizes Float fields to Python floats.

## `amount_untaxed` and `amount_total` are computed on save, not typed

After the Tab-commit on the Disc.% cell, the form renderer fires an
`onchange` that recomputes `price_subtotal` / `price_total` on the
line, and `amount_untaxed` / `amount_total` on the SO header. But the
values are only persisted after Save — `check.py` validates both
`so.amount_untaxed` and `so.amount_total` are `150.0` (from 90 + 60)
to catch oracles / agents that fill the cell but never actually save.

Seed cleared all taxes (`taxes_id=[(5,0,0)]` + supplier_taxes_id) so
the total exactly equals the untaxed amount — pricelist / tax variance
was ruled out as a confound for this task.
