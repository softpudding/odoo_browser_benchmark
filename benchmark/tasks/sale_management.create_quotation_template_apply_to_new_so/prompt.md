Go to the **Sales** app.

You must first create a reusable **Quotation Template**, then use it on a
brand-new quotation for customer **Bench Test Co**. Two products have already
been seeded:

- **Bench Widget** (list price 10.00)
- **Bench Gadget** (list price 20.00)

---

## Step 1 - Create the Quotation Template

1. From the Sales top menu, open **Configuration > Quotation Templates**.
   (This menu is visible because Quotation Templates have already been
   enabled in Settings.)
2. Click **New**.
3. Set **Quotation Template** (the big title at the top of the form) to
   **`Bench Starter Pack`** (exact spelling).
4. In the **Lines** tab, add **two product lines** using the
   **Add a product** control:
   - Line 1: product **Bench Widget**, **Quantity 5**.
   - Line 2: product **Bench Gadget**, **Quantity 2**.
   Do NOT add any sections, notes, or extra product lines.
5. **Save** the template.

---

## Step 2 - Apply the template to a new Sales Order

1. Navigate back to **Sales > Orders > Quotations** (or use the breadcrumb)
   and click **New** to start a new quotation.
2. Set **Customer** to **`Bench Test Co`**.
3. In the **Quotation Template** field on the order form, pick
   **`Bench Starter Pack`**. After you pick it, the two order lines from
   the template (Widget x5, Gadget x2) must appear automatically in the
   order lines area.
4. Do **not** touch/edit/delete any of the auto-populated lines - leave
   quantities exactly as they came from the template.
5. **Save** the quotation (cloud/save icon). Do **NOT** click **Confirm**;
   the record must stay in the **Quotation** (draft) state.

---

**Rules:**
- The quotation template name must be exactly `Bench Starter Pack`.
- The template must contain exactly two product lines (Widget qty 5,
  Gadget qty 2) - no sections, notes, or extras.
- The new sales order must be for `Bench Test Co`, have
  `Bench Starter Pack` as its Quotation Template, and end up with exactly
  two order lines matching the template.
- Do NOT confirm the sales order - leave it as a draft Quotation.
- Do NOT modify any other seeded products, customers, or existing templates.
