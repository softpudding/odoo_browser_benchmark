Open the Invoicing (Accounting) app. There are two **posted** customer invoices:

| Customer                 | Reference      |
|--------------------------|----------------|
| Greenfield Manufacturing | CN-SERVICE-01  |
| Greenfield Materials     | CN-SERVICE-02  |

The invoice for **Greenfield Manufacturing** (`CN-SERVICE-01`) needs a **partial** credit note.

Only **1 unit** of `Warehouse Audit` should be refunded.
The `Onsite Training` line should **not** be refunded.

Your job:

1. Open the posted invoice with reference `CN-SERVICE-01`.
2. Click **Credit Note**.
3. In the credit note wizard:
   - Set **Reason** to exactly: `Warehouse Audit session canceled`
   - Set **Credit Note Date** to **2026-05-05**
   - Click **Reverse** (or **Create Credit Note**)
4. You are now viewing the draft credit note. Edit it so that:
   - only the `Warehouse Audit` line remains
   - its quantity is **1**
5. Click **Confirm** to post the credit note.

**Rules:**
- Only create a credit note for `CN-SERVICE-01`
- The posted credit note must contain exactly one product line: `Warehouse Audit`
- That line must have quantity **1**
- The credit note date must be **2026-05-05**
- Do not modify or credit `CN-SERVICE-02`
- Do not cancel or delete any invoice
