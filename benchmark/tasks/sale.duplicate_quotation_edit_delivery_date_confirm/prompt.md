Go to the **Sales** app and open **Quotations**.

Find the draft quotation **S-BENCH-COPY-001** for customer **Bench Copy Co**.

1. Open the quotation by clicking its row.
2. In the control panel, click the **cog / Actions** (gear) menu and choose
   **Duplicate**. Odoo will navigate to a new draft copy with the same
   customer and the same two order lines.
3. On the **duplicated** quotation (the copy — NOT the original):
   - Set the **Delivery Date** to **08/15/2026**. The Delivery Date field
     lives on the **Other Info** tab of the order form, under the
     "Shipping" group. The field is a datetime widget; typing
     `08/15/2026` (or `08/15/2026 00:00:00`) into it is fine.
   - **Save** the form (use the cloud / save icon in the breadcrumb area
     or the form's Save button).
4. Still on the duplicate, click the **Confirm** button in the order's
   status bar (header). The duplicate's state should transition from
   Quotation to Sales Order (state='sale').

**Rules:**
- Do NOT modify, confirm, or delete the original `S-BENCH-COPY-001`
  quotation — it must stay exactly as seeded (draft, same customer,
  same two lines).
- Do NOT create a brand-new quotation from scratch — use the cog
  Actions → Duplicate flow.
- Keep both order lines on the duplicate exactly as copied:
  `Bench SO Item A` qty=2 and `Bench SO Item B` qty=3.
- Only the duplicate must be confirmed. Do not click Confirm on the
  original.
- Set the Delivery Date **before** confirming so `commitment_date`
  is persisted.
