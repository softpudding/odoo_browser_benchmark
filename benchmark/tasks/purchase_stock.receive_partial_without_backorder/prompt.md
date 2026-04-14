Open the Purchase app. There is a confirmed purchase order from vendor **North Coast Components** with source document `NOBACK-04`.

The supplier has short-shipped this order and confirmed that the remaining units will **not** be sent later.

Open the receipt for this PO and receive only these quantities:

| Product         | Ordered | Receive Now |
|----------------|---------|-------------|
| Servo Motor    | 8       | 6           |
| Sensor Harness | 12      | 9           |

Then validate the receipt.

When the backorder dialog appears, choose **No Backorder** so the missing quantities are not left on another receipt.

**Rules:**
- Do not create a backorder
- The purchase order should end with exactly one done receipt
- The ordered quantities must stay at 8 and 12 on the PO lines
- The received quantities must be exactly 6 and 9
- Do not cancel the PO
