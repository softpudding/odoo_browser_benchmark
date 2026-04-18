You are on the **Discount & Loyalty** configuration page. There is already an existing program named **`Holiday Bonus 5%`** — leave it untouched.

## Step 1 — Create a new loyalty program

Create a brand-new program with these exact values:

- **Program Name**: `Spring 10% Discount`
- **Program Type**: `Discount Code` (the type whose customers redeem with a code)
- **Conditional rule**:
  - **Code**: `SPRING10`
  - **Minimum Purchase**: `150.00` (the order subtotal must be at least 150 for the code to be accepted)
- **Reward**:
  - A single `10%` discount that **applies to the whole order** (Discount Applicability = "Order", not "Cheapest Product" or "Specific Products")
  - Set the reward **Description** to `Spring Sale Discount`

Save the program.

## Step 2 — Apply the code on the public shop cart

Navigate to the public web shop cart at **`/shop/cart`**. There is already a draft cart for the admin user containing two seeded products (`Spring Lawn Chair` × 2 and `Spring Garden Light` × 1, subtotal $200).

In the **Discount code...** field on the cart page, enter `SPRING10` and click **Apply**. A success message should confirm the code was applied and a new discount line should appear in the cart with a negative amount.

## Rules

- Do not modify, rename, archive, or delete the existing **`Holiday Bonus 5%`** program
- Do not change the seeded cart's existing two product lines (do not change quantities or remove them)
- Create exactly **one** new loyalty program named `Spring 10% Discount`; do not duplicate
- Apply the code from the public web shop cart page (`/shop/cart`) — not from the back-office sale order form
- Do not confirm or pay the order; leave it as a cart/draft sale order
