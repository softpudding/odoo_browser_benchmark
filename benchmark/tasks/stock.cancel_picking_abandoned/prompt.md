Go to the **Inventory** app.

In the left sidebar, open **Operations > Transfers** and locate the ready
outgoing delivery **`WH/OUT/BENCH-CANCEL`** — it is for customer **Bench
Cancel Ship Co** and contains one line for **Bench Cancel Prod** with demand
**3 Units**. Its current status is **Ready** (i.e. `state='assigned'`).

The warehouse team abandoned this transfer — the customer changed their
mind before shipment. You must cancel this delivery.

1. Click the row to open `WH/OUT/BENCH-CANCEL`.
2. In the form header/statusbar, click the **Cancel** button.
3. Odoo will show a confirmation dialog asking **"Are you sure you want to
   cancel this transfer?"**. Click the primary confirm button (**Ok** /
   **Confirm**) to proceed.
4. The picking status should become **Cancelled** (`state='cancel'`).

**Rules:**
- Do NOT create a new picking, return, scrap, or backorder.
- Do NOT delete the picking — it must still exist, just with
  `state='cancel'`.
- Do NOT validate the picking — you must cancel it, not transfer it.
- Do NOT modify the move lines, product, quantity, or partner.
- If any other confirmation dialog (e.g. a Document Layout config dialog)
  appears, dismiss it without interacting with the picking's data.
