# website_sale.checkout_portal_apply_coupon_complete

| Field | Value |
|---|---|
| **Status** | Done |
| **Oracle** | PASS (F1 = 1.0) |
| **Browser-Use** | PASS (F1 = 1.0) |
| **Difficulty** | hard |
| **Wall clock (oracle)** | ~70 s |
| **Wall clock (BU)** | ~66 s (12 steps) |
| **Odoo modules** | website_sale, website_sale_loyalty, sale_loyalty, loyalty, payment_custom |

## Workflow

From `/shop`, add the seeded `Bench Coupon Item` ($100) to the cart, apply the
pre-generated coupon `BENCH10CODE` in the cart's `Discount code...` input
(form `name='coupon_code'`, POST to `/shop/pricelist?r=/shop/cart`), proceed
through the auto-filled billing-address step, pick the only enabled payment
provider (Wire Transfer), and click Pay now.  The order ends up in state
`sent` with `amount_total = 90.0` (the 10% promo discount applied) and a
`payment.transaction` in `pending` on the Wire Transfer provider.

## Capability tested

- Closed-loop public-portal checkout across multiple controllers
  (`/shop`, product page, `/shop/cart`, `/shop/checkout` or `/shop/address`,
  `/shop/payment`, `/shop/confirmation`).
- Coupon application via the `coupon_form` template (inline input +
  Apply button) — distinct from the `promo_code` `program_type`
  (with_code trigger on the program rule).
- Wire Transfer payment path: the SO stays in `state='sent'` (not `sale`)
  until the admin manually confirms the transfer.

## Browser-Use trace summary

BU solved the task cleanly in 12 steps.  It signed in, opened the
product tile, clicked Add to cart, typed `BENCH10CODE`, clicked Apply,
clicked the Checkout button, confirmed the pre-filled address, selected
Wire Transfer, clicked Pay now, and landed on `/shop/confirmation`.

The task is not a BU-trap: this is a realistic end-to-end checkout
reference that the SOTA browser agent can complete when given exact
field values.  Its value for the benchmark is as a positive control +
a cross-module closed-loop spanning loyalty + website_sale + payment.
