# POS / pos_discount cookbook notes

## pos_discount (Global Discounts) is not in the base snapshot

- Module name: `pos_discount`. Seed must `button_immediate_install()` on demand
  (same pattern as `stock_dropshipping` / `survey`).
- To enable the on-screen Discount button the `pos.config` must have:
  - `module_pos_discount = True`
  - `iface_discount = True` (sometimes still referenced)
  - `discount_pc = <float>` (default percentage used by the popup)
  - `discount_product_id = <product.product id>` (an Odoo S.A. data record
    `pos_discount.product_product_consumable` is created when the module loads)
- If `module_pos_discount=True` but `discount_product_id` is unset, `pos.config.open_ui()`
  raises `UserError("A discount product is needed...")`.

## UI: the Discount button lives inside the "more" popup, not the top bar

In Odoo 19 (`addons/point_of_sale/static/src/app/screens/product_screen/control_buttons/control_buttons.xml`):

- All secondary actions (Pricelist, Refund, Fiscal position, Product Info, Cancel
  Order, plus `pos_discount`'s Discount) render only inside the `ControlButtonsPopup`
  dialog (`t-if="props.showRemainingButtons"`).
- The popup opens from the ellipsis button in the top right of the product screen
  (`button.more-btn`, inner icon `oi-ellipsis-v`).
- Playwright selector chain that works:
  ```py
  page.locator("button.more-btn, button:has(.oi-ellipsis-v)").first.click()
  page.locator(".modal:visible button.js_discount, .modal:visible button:has-text('Discount')").first.click()
  ```

## JSON-RPC oracle pattern for POS is the reliable option

The POS kiosk UI is full-screen, Owl-driven, and very timing-sensitive. The
Playwright-driven POS oracle for `point_of_sale.open_session_sell_product_cash`
is currently flaky on this machine (a `o_technical_modal` sits in the DOM and
intercepts pointer events). The `point_of_sale.split_payment_email_receipt`
oracle uses `call_kw` directly and is stable — prefer that pattern.

To create a paid POS order with a global-discount line via JSON-RPC:

```js
const lines = [
  [0, 0, { product_id, qty: 2, price_unit: 20, price_subtotal: 40,
           price_subtotal_incl: 40, tax_ids: [[6, 0, []]] }],
  [0, 0, { product_id: config.discount_product_id[0], qty: 1, price_unit: -6,
           price_subtotal: -6, price_subtotal_incl: -6, tax_ids: [[6, 0, []]] }],
];
await callKw({ model: 'pos.order', method: 'create',
               args: [[{ name: 'Bench Test Store - 000001', session_id, config_id,
                         company_id: 1, amount_total: 34, lines }]], kwargs: {} });
```

Then register payment via `pos.make.payment` with
`context: { active_id: orderId, active_ids: [orderId] }` and call `check()`.

## Browser-use solves the "apply global discount + pay cash" flow easily

On a single 15-step run, browser-use found the ellipsis Action menu, clicked the
Discount button, typed `15`, confirmed, paid Bench Cash and validated — F1=1.0.
POS global-discount-at-default-percent is NOT a hard pattern; escalate with a
non-default percentage (different from `discount_pc`), a split payment with a
discount, or a mid-order customer change before it counts as hard.
