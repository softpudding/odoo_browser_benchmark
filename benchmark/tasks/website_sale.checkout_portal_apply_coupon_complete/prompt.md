You are logged in as **admin**. The webshop is pre-seeded with a published product **`Bench Coupon Item`** priced at **$100.00** and a loyalty **Coupon** program called **`BENCH10`** that has exactly one pre-generated, redeemable coupon code: **`BENCH10CODE`** (a 10% discount on the order). **Wire Transfer** is the only enabled payment method.

Your job is to carry the order all the way through the public webshop checkout using that coupon.

## Steps

1. Open the public shop at **`/shop`** and click the product tile for **`Bench Coupon Item`**.
2. On the product page, click **`Add to cart`** (quantity `1`). If an optional-products / upsell modal appears, dismiss it without adding anything extra, then go to **`/shop/cart`**.
3. On **`/shop/cart`**, locate the **discount code** input (placeholder `Discount code...`), type **`BENCH10CODE`** exactly, and click the **`Apply`** button. A new reward line for the 10% discount must appear on the cart, bringing the total to **$90.00**.
4. Proceed through checkout: click the primary button (labelled `Checkout`, `Process Checkout` or similar — `name='website_sale_main_button'`) to move from `/shop/cart` to the address / payment step. If Odoo lands on `/shop/address` or `/shop/checkout`, accept the pre-filled billing address by clicking the primary `Save address` / `Confirm` / `Continue` button. Do NOT edit the address fields; the admin partner already has a valid US address.
5. On `/shop/payment`, select the **Wire Transfer** payment option (the only available radio), accept any Terms checkbox if present, and click **`Pay now`**.
6. When Odoo redirects you to **`/shop/confirmation`**, the task is finished. Do NOT reload or navigate back.

## Expected end state

- Exactly one `sale.order` exists for admin with `client_order_ref` unset, containing:
  - One product line for `Bench Coupon Item` at price $100.00, qty 1.
  - One loyalty reward line tied to the `BENCH10` program at -$10.00.
- The order's `amount_total` is **$90.00**.
- The order's `state` is `sale` or `sent` (Wire Transfer may leave it at `sent` until the admin manually confirms the transfer; both are acceptable).
- A `payment.transaction` for the order exists on the Wire Transfer provider (`pending` or `done`).
- The `BENCH10CODE` coupon card is marked used (`points=0` or linked via the reward line).

## Rules

- Do **not** create a new loyalty program or a new coupon — only use the seeded `BENCH10CODE`.
- Do **not** change the product quantity (keep it at 1) and do **not** add any other product to the cart.
- Do **not** abandon payment: the task is only complete when the order reaches `/shop/confirmation` and the Wire-Transfer transaction exists.
- Do **not** modify the admin partner's address, email, or phone.
