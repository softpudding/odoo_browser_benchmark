# website_sale.apply_product_filter_clear_facets — RESULT

| Field | Value |
|---|---|
| **Difficulty** | medium |
| **Oracle** | PASS (F1=1.0, 92.3s) |
| **Browser-Use** | PASS (F1=1.0, 89.0s, single-shot) |
| **Postcondition failures** | 0 |

## Workflow summary

1. Seed two `product.public.category` records (`Gadgets`, `Widgets`) plus five
   published products: Bench Gadget Mini / Plus / Pro ($30 / $80 / $150) under
   Gadgets and Bench Widget Tiny / Max ($20 / $120) under Widgets.
2. Agent navigates `/shop`, clicks the **Gadgets** category link in the sidebar
   (URL becomes `/shop/category/<slug>`), applies a **max_price = 100** price
   filter (URL becomes `/shop/category/<slug>?max_price=100`, 2 products
   visible), clears the category via **All Products** (URL becomes
   `/shop?max_price=100`, 3 products visible including Bench Widget Tiny),
   opens the Bench Widget Tiny product page and clicks **Add to cart**.
3. `check.py` finds a draft website `sale.order` whose lines reference
   `Bench Widget Tiny` (match is done by product name, not by partner, because
   `/shop` is `auth="public"` and the cart's partner depends on whether the
   agent logged in), verifies exactly one line with qty 1, and asserts that
   no Gadget or Bench Widget Max line sneaked in.

## Calibration

BU solved the task first-shot in 89 s / 14 steps. It did struggle briefly with
the dual-handle price slider — it found the right-hand number-input by clicking
the `$150` counter which exposes the hidden `<input type="number">`, typed
`100`, pressed Enter, and the `newRangeValue` handler redirected. After that
it clicked the "All products" link to strip the category segment, opened the
Widget product page and hit **Add to cart**. Kept as a tier-2 medium because
the triple interaction (path filter + query filter + query-filter-preserving
category clear) is a legitimate capability check even if the current BU model
passes it.

## New cookbook entries

See `COOKBOOK_NOTES.md` for additions to `benchmark/ODOO19_PATTERNS.md`.
