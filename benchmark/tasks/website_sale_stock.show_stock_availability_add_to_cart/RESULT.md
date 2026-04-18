# website_sale_stock.show_stock_availability_add_to_cart — RESULT

| Field | Value |
|---|---|
| **Difficulty** | medium |
| **Oracle** | PASS (F1=1.0, 54.7s) |
| **Browser-Use** | PASS (F1=1.0, 70.1s, single-shot) |
| **Postcondition failures** | 0 |

## Workflow summary

1. Seed installs the `website_sale_stock` bridge (plus `sale_stock` + `stock_delivery`)
   via `button_immediate_install`, then creates one storable product
   `Bench Limited Stock` (list_price 40.0, `is_storable=True`,
   `show_availability=True`, `available_threshold=100`,
   `allow_out_of_stock_order=True`, `is_published=True`). Five units are
   placed at WH/Stock via `stock.quant._update_available_quantity`.
2. Agent navigates `/shop`, clicks through to the product page, bumps
   the `#add_qty` input to 3, clicks **Add to cart**. With
   `threshold=100` and `free_qty=5`, the yellow
   `#threshold_message` badge (`5.0 Units in stock`) renders on the
   product page — that banner is the visual hook mentioned in the prompt.
3. `check.py` finds a draft website `sale.order` whose lines reference
   `Bench Limited Stock`, verifies exactly one line with
   `product_uom_qty == 3`, and asserts the product still carries
   `show_availability=True` / `available_threshold=100`.

## Calibration

BU solved it first-shot (70 s / PASS + F1 1.0). The banner + qty=3
combo turned out to be trivial for the current BU model: the
`add_qty` input is a straightforward `<input>` widget (no dual-handle
slider, no modal), and Odoo's shop page renders the quantity box
directly adjacent to the Add-to-cart CTA.

Per the task spec's fallback clause ("If the cap-at-5 enforcement is
not a separate behavior, reduce the task to just 'add qty=3 and
verify availability shown'"), this is the version we shipped:
`allow_out_of_stock_order=True` means the 5-unit on-hand is *not* a
hard cap (BU could type 999 and still add), but the seeded value
deliberately stays within 5 so the availability banner remains
coherent with the prompt's description. The banner's existence is
verified indirectly via the `show_availability` assertion in check.py
and via the qty-limit narrative in prompt.md.

## New cookbook entries

See `COOKBOOK_NOTES.md` for additions to `benchmark/ODOO19_PATTERNS.md`
about website_sale_stock install dependencies and the
`threshold_message` banner mechanics.
