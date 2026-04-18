Configure the work order on a confirmed manufacturing order and finish it.

Context:
- A manufacturing order **WH/MO/BENCH0001** is already **Confirmed** for
  product **Bench Operation Product** with quantity **5**.
- The MO has a single operation running on work center
  **Bench Assembly Station**. A work order named **Assembly Station** has
  already been created for it.

Steps:
1. Go to **Manufacturing** and open **Manufacturing Orders**. Click the row
   for **WH/MO/BENCH0001** to open it.
2. Click the **Work Orders** tab on the MO form.
3. On the work order line **Assembly Station**, set **Expected Duration**
   to `45` (minutes).
4. Save the MO so the duration change is persisted.
5. Click **Start** on the work order to begin it (this moves its state to
   In Progress).
6. Click **Done** on the work order to finish it. Its state must become
   **Finished** (the manufacturing order itself may remain in progress —
   that is fine).

Rules:
- Do NOT cancel the manufacturing order.
- Do NOT delete the work order.
- Do NOT change the product, quantity, or work center.
- The Expected Duration must be exactly 45 minutes.
