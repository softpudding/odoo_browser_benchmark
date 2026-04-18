Navigate to the **Sales** app and open the **Quotations** list.

Find the draft quotation with customer reference **"S-BENCH-STK-001"** for
customer **Bench Warehouse Co**. The quotation has a single line:

| Product              | Ordered Qty |
|----------------------|-------------|
| Bench Limited Widget | 10          |

The warehouse has **5** units of **Bench Limited Widget** on hand, less than
the 10 ordered. The customer has agreed to receive only **2** units in the
first shipment (even though more are reservable) and the remaining **8**
units will be sent in a backorder.

### Steps

1. Open the quotation and click **Confirm** to convert it into a Sales Order.
   If any warning dialog appears about insufficient stock, dismiss it /
   confirm anyway so the sale order becomes confirmed.
2. Click the **Delivery** smart button to navigate to the delivery order.
3. On the delivery order, the **Done** quantity for **Bench Limited Widget**
   will be auto-filled to the reserved amount (5). You MUST change the
   **Done** quantity to **2**.
4. Click **Validate**.
5. A backorder dialog will appear asking what to do with the unshipped 8
   units. Click **Create Backorder** (do NOT click "No Backorder").

### Final state

- Sales order **S-BENCH-STK-001** is confirmed (state = "Sales Order").
- The first delivery is **Done** with Done quantity = **2**.
- A **backorder** delivery exists (state Ready/Waiting/Assigned) for the
  remaining **8** units of Bench Limited Widget.

### Rules

- You MUST set the Done quantity on the first delivery to exactly **2**
  (not 5, not 10).
- You MUST choose **Create Backorder** in the dialog — do NOT choose
  "No Backorder".
- Do NOT cancel the order or the delivery.
- Do NOT modify any other quotation or sales order.
- Do NOT change the products, customer, or prices on the order.
