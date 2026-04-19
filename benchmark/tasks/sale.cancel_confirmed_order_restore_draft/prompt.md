Go to the **Sales** app and open **Orders**.

Find the confirmed sales order whose **Customer Reference** is
**BENCH-CANCEL-RESTORE** for customer **Bench Cancel Co**. It currently has
status **Sales Order** (confirmed, `state='sale'`).

1. Open the order by clicking its row.
2. In the order form's statusbar header, click the **Cancel** button.
3. Odoo shows a confirmation dialog: "Are you sure you want to cancel this
   order? This may affect related documents or processes." Click **Ok** (or
   the primary confirm button) to proceed with cancellation. The order's
   state should become **Cancelled**.
4. The statusbar now shows a **Set to Quotation** button (only visible on
   cancelled orders). Click **Set to Quotation** to return the order to
   draft.

**Rules:**
- Do NOT create a new sale order — you must reuse the existing
  `BENCH-CANCEL-RESTORE` order for Bench Cancel Co.
- Do NOT delete the order at any point.
- Do NOT touch the order lines — both seeded lines (Bench Cancel Item A
  qty=2 and Bench Cancel Item B qty=3) must remain exactly as seeded.
- The final state of the order must be **Quotation** (`state='draft'`).
  Not `cancel`, not `sale`, not `sent` — draft.
- If you see a "Document Layout" configuration dialog at any point, dismiss
  it without modifying the order.
