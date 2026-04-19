Go to the **Purchase** app and open **Orders → Requests for Quotation**.

Find the draft RFQ **BENCH-VCODE** for vendor **Bench Code Supplier** and
open it. It already has exactly one order line for product
**Bench Widget** with **Quantity = 5**. The Description currently just
shows the product name `Bench Widget`.

Your task is to **add a vendor product code description** to that line:

1. In the **Products** tab (Order Lines), click into the Bench Widget
   row's **product / description** cell (the merged cell on the left
   that shows the product name "Bench Widget"). The row enters edit
   mode.
2. Reveal / focus the description textarea. In Odoo 19 the editable
   list merges the Product name and Description into the same cell —
   if no description is shown yet, click the small icon next to the
   product name (tooltip: "Click or press enter to add a description")
   to reveal a description text area just below the product name.
3. Type into the description area exactly:

   ```
   BENCH-WDG-A1 / Bench Widget
   ```

4. Press **Tab** (or click elsewhere) to commit.
5. **Save** the RFQ using the cloud/save icon (or the breadcrumb Save
   button). Do NOT click **Confirm Order**.

The stored description may appear with the product name prepended
(rendered on two lines) — that is normal Odoo 19 behaviour for this
widget. What matters is that the vendor code `BENCH-WDG-A1` ends up
in the line's Description.

**Rules:**

- Edit only the **Description** on the existing Bench Widget line.
- Do NOT change the Product, Quantity, Unit Price, Taxes, or
  Expected Arrival.
- Do NOT confirm the order — it must stay in the **RFQ** (draft) state.
- Do NOT delete or re-add the line.
- The substring `BENCH-WDG-A1` must appear in the saved Description.
