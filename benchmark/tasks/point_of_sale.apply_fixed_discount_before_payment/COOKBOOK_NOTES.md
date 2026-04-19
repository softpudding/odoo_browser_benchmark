# point_of_sale.apply_fixed_discount_before_payment — Odoo 19 quirks

## pos_discount is not in the base snapshot

- Module name: `pos_discount`. Seed must `button_immediate_install()` on demand.
- To enable the on-screen global Discount button the `pos.config` must have:
  - `module_pos_discount = True`
  - `iface_discount = True`
  - `discount_pc = <float>` (default percentage pre-filled in the popup)
  - `discount_product_id = <product.product id>` (Odoo S.A. provides
    `pos_discount.product_product_consumable` via data file)
- If any of these is missing, `pos.config.open_ui()` raises `UserError`.

## Global Discount is PERCENT-only, never fixed currency

`pos_discount.ControlButtons.clickDiscount` opens a `NumberPopup` titled
"Discount Percentage" whose payload is parsed as percent and clamped
0–100. There is NO fixed-currency mode built into pos_discount. To apply
a "fixed EUR" discount via this button you must pick a percentage that
*rounds* to the target currency amount against the exact subtotal.

For this task the trick is:
- subtotal = 35.00 (20 + 15)
- desired discount = 5.00 EUR
- required percent = 5 / 35 = 14.2857…% → seed `discount_pc=14.29`
- 14.29 × 35.00 = 5.0015 → rounded to 2dp = 5.00

Because the popup is **pre-filled** with `discount_pc`, the agent just
confirms the default. Agents that re-type the percentage can introduce
rounding drift; prompt should explicitly say "accept the pre-filled 14.29".

## UI: the Discount button lives inside the "more" popup, not the top bar

Odoo 19 `addons/point_of_sale/static/src/app/screens/product_screen/control_buttons/control_buttons.xml`
renders all secondary actions inside `ControlButtonsPopup` which opens
from the ellipsis button `button.more-btn` (inner `.oi-ellipsis-v`).
Human prompt must mention "open the Actions / ellipsis menu in the
top-right" or humans miss the button.

## JSON-RPC oracle bypass

As with `point_of_sale.add_item_apply_global_discount_pay_cash` and
`point_of_sale.split_payment_email_receipt`, the Playwright-driven POS
oracle is flaky (`o_technical_modal` intercepts pointer events). The
stable pattern is to create the `pos.order` with all three lines
(2 product + 1 discount using `config.discount_product_id`) via
`call_kw`, then run `pos.make.payment.create` + `.check` with
`context={active_id, active_ids:[orderId]}` to close the order.

```js
const lines = [
  [0, 0, { product_id: productA, price_unit: 20, qty: 1, ... }],
  [0, 0, { product_id: productB, price_unit: 15, qty: 1, ... }],
  [0, 0, { product_id: discountProductId, price_unit: -5, qty: 1, ... }],
];
```

## Check tolerances

`amount_total` ± 0.2 and discount line `price_subtotal_incl` ± 0.5 are
enough to absorb the 14.29% rounding drift across both oracle and UI
paths. `qty` is strict (±0.0001) because POS does not round it.

## Browser-use solves this task easily — calibrates easier than hard

Single-shot BU run: 111s, PASS, F1=1.0. BU found the ellipsis Action
menu, opened Discount, kept the pre-filled 14.29, paid Bench Cash 30.00
and validated. Same lesson as `point_of_sale.add_item_apply_global_discount_pay_cash`:
POS global-discount-then-pay-cash is not a hard pattern on modern BU,
even with non-default decimal percentages pre-filled. **Escalation ideas**:
split payment (Cash + Bank) with a discount, mid-order customer change
before the discount, or force the popup to NOT be pre-filled (reset
`discount_pc=0`) so the agent must type a specific multi-decimal value.

## Seed pitfall: tax_ids needs to be cleared on both product.product AND template

Setting `taxes_id=[(5,0,0)]` only on `product.product` still leaves the
product_tmpl_id with company-default taxes that re-apply on POS load.
Always clear on both:
```python
product.write({"taxes_id": [(5, 0, 0)]})
product.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})
```
