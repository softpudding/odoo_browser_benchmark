Navigate to the **Sales** app and open the **Orders** list.

Find the confirmed sales order with customer reference **`S-BENCH-DS-001`** for
customer **Bench Dropship Buyer**. The order has 1 line:
**Bench Dropship Gadget** quantity **5**.

Because the product is configured with the **Dropship** route, confirming the SO
has already created a draft purchase order (RFQ) for vendor
**Bench Dropship Supplier** and a dropship transfer that ships goods directly
from the vendor to the customer.

Complete the workflow as follows:

1. Open the SO `S-BENCH-DS-001`.
2. Click the **Purchase** smart button at the top of the SO to navigate to the
   auto-generated draft RFQ for **Bench Dropship Supplier**.
3. On that RFQ (state = RFQ / draft), click **Confirm Order** to convert it into
   a purchase order (state must become "Purchase Order").
4. From the confirmed PO, click the **Dropship** smart button at the top of
   the PO to open the linked dropship transfer (the picking type is
   "Dropship", not a standard customer delivery or vendor receipt).
5. On the dropship transfer, set the **Done** quantity for
   **Bench Dropship Gadget** to **5** (matching the demand).
6. Click **Validate** to mark the dropship transfer as Done.
   - If a backorder dialog appears, choose **No Backorder** (the full quantity
     is being shipped, no backorder is needed).

**Final state required:**
- Sales Order `S-BENCH-DS-001` remains confirmed (state = "Sales Order"); its
  Bench Dropship Gadget line shows **Delivered = 5**.
- The Purchase Order for vendor Bench Dropship Supplier has state =
  "Purchase Order".
- The dropship transfer is in state "Done" with **5** units delivered.

**Rules:**
- Do NOT cancel the SO, the PO, or the picking.
- Do NOT change the vendor, the customer, the product, the prices, or the
  ordered quantity (5).
- Do NOT create a separate customer delivery — use the dropship transfer that
  was generated automatically.
- Do NOT create a backorder; ship the full quantity.
