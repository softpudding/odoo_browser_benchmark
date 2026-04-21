You are on the backend **Sales > Configuration > Discounts & Loyalty** list (`/odoo/discount-loyalty`). The database has a draft sales order **`SO-BENCH-001`** for customer **`Bench Promo Customer`** with one product line (**`Bench Promo Product`**, qty 1, unit price €100.00, no taxes). The order subtotal and total are currently €100.

You must create a new promo-code program in the backend, then apply that code to the seeded draft order so the total becomes €90.

## Step 1 - Create the Discount Code program

From the **Discounts & Loyalty** list, create a new program with these exact values:

- **Program Name**: `Bench Promo 10%`
- **Program Type**: `Discount Code` (the type that requires customers to enter a code; `program_type='promo_code'`)
- On the **Conditions / Rules** tab, set the single rule's **Promo Code** to: `BENCH10`
- On the **Rewards** tab, configure the single reward as: **Discount**, **10%** off, **Apply On: Order** (i.e. the whole order, not specific products). Leave `discount_mode` as `percent`.

**Save** the program.

## Step 2 - Apply the promo code to the seeded sales order

Open **Sales > Orders > Quotations** and find the draft quotation **`SO-BENCH-001`** (customer: `Bench Promo Customer`).

On the order form, apply the promo code `BENCH10` using the **Coupon Code** button in the form header.

After applying, a new order line should appear labeled as a **Discount** (reward line) with a **negative** amount of **-€10.00**. The order **Total** should drop from €100.00 to **€90.00**. **Save** the order.

## Rules

- Leave the order in **draft** state (do **not** confirm it, do **not** send by email)
- Do **not** modify the product line (do not change quantity or unit price)
- Do **not** create or delete other sales orders, other loyalty programs, or other products
- The promo code must be **exactly** `BENCH10` (uppercase, no trailing space)
- Discount must be **10%** on the **whole order** (not per-product, not a fixed amount)
