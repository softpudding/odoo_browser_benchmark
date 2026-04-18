Go to the **Sales** app.

Create a new **quotation** for customer **Bench Premium Co**. This customer
already has the **"VIP 20% Off"** pricelist assigned on their contact record,
so it should apply automatically when you pick them.

Fill in the quotation as follows:

1. Set **Customer** to **Bench Premium Co**. After picking them, the
   **Pricelist** field in the order header should auto-populate with
   **"VIP 20% Off"**. Leave it on that pricelist — do **not** change it to
   another pricelist and do **not** clear it.
2. Add a single order line:
   - Product: **Bench Standard Widget**
   - Quantity: **5**
   Let Odoo compute the unit price from the pricelist — do **not** type in
   a price manually. The list price of this product is 100.00, so the
   pricelist-driven **Unit Price should show 80.00** (20% off).
3. **Save** the quotation (click the cloud/save icon or press the
   form's save button). Do **NOT** click **Confirm** — the record must
   stay in the **Quotation** (draft) state.

**Rules:**
- Do not confirm the quotation (leave it as a draft Quotation).
- Do not change the pricelist away from "VIP 20% Off".
- Do not add extra order lines or extra products.
- Do not manually override the unit price on the line; it must come from
  the pricelist (80.00).
