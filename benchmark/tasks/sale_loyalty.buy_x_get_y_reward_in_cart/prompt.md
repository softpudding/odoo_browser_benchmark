You are on the backend **Sales > Configuration > Discounts & Loyalty** list (`/odoo/discount-loyalty`).

The database has:

- A **Buy X Get Y** loyalty program named **`Bench BOGO`** already configured and **active**. The program is set up as *Buy 2 Get 1 Free on **Bench Promo Widget***. Its trigger is **Automatic**, program type **Buy X Get Y**, rule min quantity 2, reward free-product qty 1, required points 2.
- A customer **`Bench Promo Customer`**.
- A product **`Bench Promo Widget`** priced at **€10.00** (no taxes).

**Your task:**

## Step 1 - Create a quotation with 2 widgets

Go to **Sales > Orders > Quotations** and create a **new quotation** with:

- **Customer**: `Bench Promo Customer`
- **Order line** (one line): product `Bench Promo Widget`, **quantity 2**, unit price €10.00 (default from product).

Save the quotation.

## Step 2 - Claim the free-product reward

On the saved quotation, the **Buy 2 Get 1 Free** reward should now be claimable. Claim the reward using the **reward wizard / "Claim Reward" action** available from the order form:

- Open the reward wizard (sometimes offered as an automatic notification after save, sometimes via the *Coupons & Promotions* / *Claim Reward* button).
- Select the **`Bench BOGO`** reward (the Free-Product reward for Bench Promo Widget).
- **Apply** the reward.

A new **reward line** for Bench Promo Widget (qty 1, marked as reward) must appear on the order. The free line is added by Odoo with a price effectively zero (the product line at 0.0 or the reward amount nets it out to -€10.00, depending on the UI — do not edit these values manually).

## Step 3 - Confirm the order

Click **Confirm** on the quotation. The order state must become **Sales Order** (`state='sale'`).

## Rules

- The final confirmed order **must have exactly 2 order lines**: 1 paid widget line (qty 2) + 1 reward line for the free widget (qty 1, `is_reward_line=True`). Odoo's reward engine adds the free line automatically — do not add or edit it manually.
- **`amount_total` must equal exactly €20.00** (only the 2 paid widgets are billed; the reward line nets to 0 via 100% discount).
- Do **not** modify the seeded loyalty program, customer, or product.
- Do **not** add a third paid widget manually — the reward line must come from the promotion.
- Do **not** create, delete, or modify any other sale order or loyalty program.
- Leave the confirmed sale order active (do **not** cancel it).
