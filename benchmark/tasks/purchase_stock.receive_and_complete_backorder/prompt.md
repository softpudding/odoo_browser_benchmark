Open the Purchase app. There is a confirmed purchase order from vendor **Stellar Supplies** with source document `BENCH-PARTIAL`.

This PO has two product lines:

| Product           | Ordered Qty |
|-------------------|-------------|
| Copper Wire Spool | 10          |
| Steel Bracket     | 20          |

Your job is to **receive the goods in two batches** and make sure both receipts end up as Done:

### Batch 1 — partial receipt
1. Open the PO and click **Receive Products** (or find the associated receipt in Inventory).
2. In the receipt form, change the received quantity (**Done** column) to:
   - Copper Wire Spool: **4**
   - Steel Bracket: **8**
3. Click **Validate**. A dialog will ask about the remaining quantities — choose **Create Backorder**.

### Batch 2 — complete the backorder
4. A new receipt (the backorder) is created automatically for the remaining quantities (Copper Wire Spool: 6, Steel Bracket: 12).
5. Open that backorder receipt.
6. Set the Done quantities to the full remaining demand (6 and 12).
7. Click **Validate** to mark it Done.

After both receipts are validated, the PO should show **Received** status (fully received).

**Rules:**
- Do not modify the PO lines or create new POs
- Do not cancel any receipt
- Both receipts must end in Done status
