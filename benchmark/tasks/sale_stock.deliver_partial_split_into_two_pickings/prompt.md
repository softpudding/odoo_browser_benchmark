Navigate to the **Sales** app and open the **Quotations** list.

Find the draft quotation with customer reference **"S-BENCH-SPLIT-001"** for
customer **Halberd Industries**. It has two product lines:

- **Halberd Alpha Module** (ProdA): ordered 5
- **Halberd Beta Module** (ProdB): ordered 8

Do the following exactly:

1. Open the quotation and click **Confirm** to convert it into a Sales Order.
   If a stock-availability warning dialog appears, dismiss it (click
   **Confirm** or **Ok**).
2. Click the **Delivery** smart button to open the delivery order.
3. On the delivery order, the **Done** column will auto-fill from reservation.
   Set the final **Done** quantities as follows (you may need to manually
   change the Beta value down):
   - **Halberd Alpha Module**: Done = **5** (full delivery)
   - **Halberd Beta Module**: Done = **3** (partial delivery — leave 5 for
     a later shipment)
4. Click **Validate**.
5. In the backorder dialog that appears, click **Create Backorder**
   (do NOT click "No Backorder").
6. After the backorder is created, the original delivery is marked Done.
   Open the **new backorder picking** for this same SO. You can find it by
   clicking the **Delivery** smart button again from the SO and selecting
   the picking that is **NOT** in state Done (the one in state Ready /
   Waiting / Assigned).
7. On that backorder picking, the system will have auto-reserved **5** units
   of **Halberd Beta Module** in the Done column. **Edit the Done quantity
   from 5 to 0** for Halberd Beta Module, then **save** the picking
   (click the cloud / save icon in the top control panel — do **NOT**
   validate; leave the backorder in its assigned/draft state).

**Rules:**
- You MUST set Done=5 for Alpha and Done=3 for Beta on the original picking.
- You MUST choose **Create Backorder** in the dialog — do NOT choose
  "No Backorder".
- On the backorder, you MUST change the Done qty for Halberd Beta Module to
  0 and save (do NOT click Validate on the backorder).
- Do NOT modify any other quotation, sales order, or picking.
- Do NOT change the products, customer, or prices on the order.
