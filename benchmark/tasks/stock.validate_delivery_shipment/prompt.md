Go to the **Inventory** app.

From the main Inventory overview, open the **Delivery Orders** (outgoing)
card — or navigate via **Operations > Transfers** and filter by the
**Delivery Orders** operation type.

Find the ready delivery with reference **"BENCH-DEL-01"** for customer
**Azure Interior**. It has two move lines:

- **Steel Bracket 12"** — demand: 20
- **Copper Wire 100m** — demand: 8

1. Open the delivery.
2. Set the **Done** quantity on the move lines to:
   - **Steel Bracket 12"**: `12`
   - **Copper Wire 100m**: `5`
3. Click **Validate**.
4. A backorder dialog appears because not everything was shipped. In that
   dialog, choose **No Backorder** to close the delivery without creating
   another transfer.

**Rules:**
- Do NOT touch the other delivery in the list (`BENCH-DEL-OTHER`).
- Do NOT change the products, partner, or scheduled date.
- Do NOT cancel the delivery.
