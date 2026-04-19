You are on the public **Shop** page (`/shop`). A website product named **`Bench Portal Product`** is already published at list price **€25.00**. No order exists yet.

You must place an order end-to-end from the web shop: add the product to the cart, go to checkout, fill the delivery address, and confirm the order using the offline **Wire Transfer** payment provider so the resulting sale order ends up in a confirmed (non-draft) state on the backend.

## Step 1 - Add the product to the cart

From the `/shop` listing, open **`Bench Portal Product`** and click **Add to Cart** (quantity 1). Then go to the cart (`/shop/cart`).

## Step 2 - Checkout: fill the delivery address

Click **Checkout** / **Process Checkout**. On the address form, fill these exact values:

- **Name**: `Bench Portal Customer`
- **Street**: `12 Bench Street`
- **City**: `Benchtown`
- **Zip**: `90001`
- **Country**: `United States`
- **Email**: `bench.portal@example.com`
- **Phone**: `+1 555-0199`

Click **Next** / **Save address**.

## Step 3 - Confirm and pay with Wire Transfer

On the payment step, choose **Wire Transfer** (the offline "pay by bank transfer" option), then click **Pay now** / **Confirm order** so the order transitions out of the `draft` quotation state on the backend.

After the confirmation page appears, the backend **sale.order** for customer `Bench Portal Customer` must have:

- `state` in (`sale`, `sent`, `done`) — i.e. **not** `draft` or `cancel`
- exactly **one** order line for `Bench Portal Product` with qty **1** at €25.00
- `amount_total` = **€25.00**
- `website_id` set (it must have been placed via the webshop)

## Rules

- Use **exactly** the values above for name/street/city/zip/country/email/phone.
- Do **not** change the product price or quantity.
- Do **not** create additional products, additional partners named `Bench Portal Customer`, or other sale orders.
- The payment provider you pick must be the offline **Wire Transfer** one (`custom` / `wire_transfer`); do not invent a credit-card transaction.
- Leave the order confirmed on the backend; do not cancel it.
