You are on the **Gift Cards & eWallet** configuration page in the back office. The shop has a draft cart for the admin user (visible at `/shop/cart`) containing one product **`Spring Premium Bundle`** at €100 (subtotal €100). The agent must configure a brand-new gift-card program, generate exactly one gift-card code with a value of 50, then go to the cart and pay €50 of it with that gift card.

## Step 1 — Create a new Gift Card program

From the **Gift Cards & eWallet** list, create a new program with these exact values:

- **Program Name**: `Spring Gift Card`
- **Program Type**: `Gift Card` (the type that issues redeemable card codes)
- Leave the other defaults (1 reward = "Gift Card" discount, "applies on" = future orders, trigger = automatic).

**Save** the program.

## Step 2 — Generate one gift-card code

On the saved program form, click the **Generate Gift Cards** button (in the form header / cog menu — labeled `Generate Gift Cards`). In the wizard:

- **For**: leave on **Anonymous Customers** (the default)
- **Quantity to generate**: `1`
- **Gift Card value**: `50`
- **Description**: `Spring Promo Gift Card`

Click **Generate Gift Cards** to issue the card. After it succeeds, open the program's **Gift Cards** smart button and **copy the code** of the single card that was just generated (you'll need to paste it into the cart in the next step).

## Step 3 — Apply the gift card code on the public shop cart

Navigate to the public web shop cart at **`/shop/cart`**. The cart already contains **`Spring Premium Bundle`** × 1, subtotal €100. In the **Discount code...** field on the cart page, paste the code copied in Step 2 and click **Apply**.

A new line should appear in the cart (a "Pay with Gift Card" / discount-style reward line) and the **Total** should drop from €100 to **€50**.

## Rules

- Do **not** modify, rename, archive, or delete the existing default **`Gift Cards`** program (the demo program shipped by Odoo) — only create the brand-new `Spring Gift Card` program
- Do **not** change the seeded cart's product line (do not change quantity, do not remove `Spring Premium Bundle`)
- Generate **exactly one** gift card on the new program (Quantity = 1, value = 50)
- Apply the gift card code from the public web shop cart page (`/shop/cart`) — not from the back-office sale order form
- Do **not** confirm or pay the order; leave it as a draft cart with the gift-card reward applied
