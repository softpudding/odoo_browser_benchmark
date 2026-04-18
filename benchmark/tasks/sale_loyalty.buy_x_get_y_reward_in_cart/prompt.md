You are on the **Discount & Loyalty** configuration page. There is already an existing program named **`Winter Bundle 3%`** — leave it untouched.

## Step 1 — Create a new loyalty program

Create a brand-new program with these exact values:

- **Program Name**: `Buy 2 Widgets Get 1 Gadget`
- **Program Type**: `Promotions` (the type where rewards apply automatically once rule conditions are met — NOT Discount Code, NOT Coupons)

### Conditional rule

Open the rule editor (pencil / gear icon on the single default rule, or "Add a rule") and set:

- **Minimum Quantity**: `2`
- **Products** (the "Among" / products-to-buy list): `Bench Widget` (this is the product the customer must buy)
- Leave **Code**, **Minimum Purchase** and other fields at their defaults.

### Reward

Open the reward editor and set:

- **Reward type**: `Free Product` (the product variant — NOT a discount)
- **Quantity rewarded**: `1`
- **Product** (the "Among" product field): `Bench Gadget`
- Set the reward **Description** to `Free Bench Gadget`.

Save the program. After saving, the program must be **active** (not archived).

## Step 2 — Verify the free reward appears in the public cart

Navigate to the public web shop cart at **`/shop/cart`**. There is already a draft cart for the admin user containing two units of `Bench Widget` (subtotal $200).

As soon as the cart page loads, the free-product reward must be auto-applied: a new line for **`Bench Gadget`** should appear in the cart at a zero total (marked as a free / 100% discount reward line). If it does not appear immediately, reload the cart page once.

You do NOT need to add the gadget manually — the promotion must trigger the free line automatically because the rule (buy 2 widgets) is satisfied.

## Rules

- Do not modify, rename, archive, or delete the existing **`Winter Bundle 3%`** program.
- Do not change the seeded cart's existing Bench Widget line quantity (keep it at exactly 2).
- Create exactly **one** new loyalty program named `Buy 2 Widgets Get 1 Gadget`; do not duplicate.
- The reward must be a product reward giving 1 `Bench Gadget` — not a percent/money discount.
- The rule's "Among" products list must contain `Bench Widget` — otherwise the rule matches every product and the task is misconfigured.
- Do not confirm or pay the cart; leave it as a draft sale order.
