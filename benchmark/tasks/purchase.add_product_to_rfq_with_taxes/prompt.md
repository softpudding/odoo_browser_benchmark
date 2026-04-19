Go to the **Purchase** app and open **Orders → Requests for Quotation**.

Find the draft RFQ **BENCH-ADD-TAX** for vendor **Bench Tax Vendor** and
open it. It already has exactly one order line for product
**Bench Other Item** with **Quantity = 2** and **no taxes** — leave that
line alone.

Your task is to **add a new line** with a taxable product:

1. In the **Products** tab (Order Lines), click **Add a product** (the
   link at the bottom of the lines list).
2. In the new row's Product cell, pick **Bench Taxable Item** from the
   autocomplete dropdown.
3. Set the new row's **Quantity** to `3`.
4. Set the new row's **Taxes** column to **Bench Tax 5%**. Click into
   the Taxes cell, type `Bench Tax 5%`, and pick it from the dropdown
   (it is a many2many tag — the tax appears as a pill in the cell).
5. **Save** the RFQ using the cloud/save icon (or the breadcrumb Save
   button). Do NOT click **Confirm Order**.

**Rules:**

- Do NOT modify the existing Bench Other Item line (product, quantity,
  taxes must all stay as seeded).
- Do NOT confirm the order — it must stay in the **RFQ** (draft) state.
- Do NOT delete any lines.
- The new line must have product=**Bench Taxable Item**, quantity=**3**,
  and Taxes containing **Bench Tax 5%**. The unit price can be left at
  the default that appears when you pick the product.
