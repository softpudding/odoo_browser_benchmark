Go to the **Sales** app and open **Quotations** (or **Orders**).

Find the **confirmed** sales order whose **Customer Reference** is
**BENCH-DUP** for customer **Bench Orig Co**. It currently has status
**Sales Order** (confirmed, `state='sale'`). A second partner named
**Bench Clone Co** already exists in the database.

1. Open the order by clicking its row.
2. In the control panel, click the **cog / Actions** (gear) menu and
   choose **Duplicate**. Odoo will navigate to a brand-new **draft** copy
   that starts with the same Customer (Bench Orig Co) and the same two
   order lines as the original.
3. On the **duplicated** order (the copy — NOT the original):
   - Change the **Customer** many-to-one field from **Bench Orig Co** to
     **Bench Clone Co**. Click the Customer field, clear it (or select
     the existing value), type `Bench Clone Co`, and pick
     `Bench Clone Co` from the autocomplete dropdown.
   - **Save** the form (use the cloud / save icon in the breadcrumb area
     or the form's Save button). The copy must remain in **Quotation**
     status (`state='draft'`).

**Rules:**
- Do NOT modify, cancel, confirm, reset, or delete the original
  `BENCH-DUP` confirmed order — it must stay exactly as seeded (state
  `sale`, customer `Bench Orig Co`, same two lines).
- Do NOT create a brand-new quotation from scratch — use the cog
  Actions → Duplicate flow.
- Do NOT click **Confirm** on the copy. The copy's final state must be
  **Quotation** (`state='draft'`). Not `sale`, not `sent`, not `cancel`
  — draft.
- Keep both order lines on the duplicate exactly as copied:
  `Bench SO Dup Item A` qty=2 and `Bench SO Dup Item B` qty=3.
- If you see a "Document Layout" configuration dialog at any point,
  dismiss it without modifying the order.
