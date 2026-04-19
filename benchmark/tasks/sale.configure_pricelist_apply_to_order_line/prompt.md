Go to the **Sales** app.

This task has **two stages**: first you must create a new **Pricelist** with a
10%-off formula rule, then you must apply that pricelist to a brand-new
quotation for the seeded customer **Bench Price Co**. Both the product
(`Bench Price Item`, list price 200.00) and the customer have already been
seeded. The Pricelists feature is already enabled in Settings so the menu is
visible.

---

## Step 1 - Create the Pricelist

1. From the Sales top menu, open **Products > Pricelists**.
2. Click **New** to create a new pricelist.
3. Set the pricelist **Name** (the big title at the top of the form) to
   **`Bench 10% Off`** (exact spelling).
4. In the **Sales Prices** tab, click **Add a line** to add a pricelist rule.
   A **"Pricelist Rule"** dialog / form opens with these nested controls.
   Configure it as follows:
   - **Apply To** (radio buttons): leave on **Product** (the default) and
     leave the **product field empty** so the rule applies to *All Products*.
     (Do NOT select a specific product or category.)
   - **Price Type** (radio buttons): pick **Formula** (NOT "Discount" and
     NOT "Fixed Price").
   - In the **formula** section that appears below, leave **Based price** on
     **Sales Price**, and set the **Discount** field to **`10`** (meaning
     10 %). Leave Round off, Extra Fee, Min/Max Margin on their defaults.
   - Save / confirm the rule (click "Save & Close" in the dialog, or click
     somewhere outside the rule row if it is inline-editable, so the rule
     is committed to the list).
5. **Save** the pricelist (cloud/save icon).

---

## Step 2 - Apply the pricelist to a new Sales Order

1. Navigate back to **Sales > Orders > Quotations** and click **New** to
   start a new quotation.
2. Set **Customer** to **`Bench Price Co`**.
3. In the **Pricelist** field on the order header, pick **`Bench 10% Off`**
   (the pricelist you just created).
4. In the Order Lines tab, click **Add a product** and add a single line:
   - Product: **`Bench Price Item`**
   - Quantity: **1**
   Let Odoo compute the unit price from the pricelist. Because the rule is
   10 % off the 200.00 sales price, the **Unit Price should auto-fill to
   180.00**. Do **NOT** manually type a price in the Unit Price cell.
5. **Save** the quotation (cloud/save icon). Do **NOT** click **Confirm**;
   the record must stay in the **Quotation** (draft) state.

---

**Rules:**

- Pricelist name must be exactly `Bench 10% Off`.
- The rule must use **Price Type = Formula** with **10%** in the formula's
  **Discount** field based on **Sales Price** (NOT the top "Discount"
  (percentage) price type, which lives in a different sub-section).
- The rule must apply to **All Products** (no product / no category).
- The new quotation must be for `Bench Price Co`, have
  `Bench 10% Off` as its Pricelist, and contain exactly one line
  (`Bench Price Item`, qty 1, unit price 180.00).
- Do NOT confirm the quotation - leave it as a draft Quotation.
- Do NOT manually override the unit price; it must come from the pricelist
  (180.00).
- Do NOT add extra rules, lines, sections, or notes.
