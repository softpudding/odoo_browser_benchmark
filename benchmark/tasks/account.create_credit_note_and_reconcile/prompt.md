Open the Invoicing (Accounting) app. There are two **posted** customer invoices:

| Customer          | Reference    | Total     |
|-------------------|--------------|-----------|
| Lakeview Partners | CN-TARGET-01 | 1,800.00  |
| Lakeview Projects | CN-IGNORE-01 | 2,400.00  |

The invoice for **Lakeview Partners** (reference `CN-TARGET-01`) needs a **partial** credit note — only 10 out of 18 units of "Professional Services" should be credited (the other 8 units were actually delivered).

Your job:

1. Open the posted invoice with reference `CN-TARGET-01` (customer: Lakeview Partners).
2. Click the **Credit Note** button.
3. In the credit note wizard:
   - Set the **Reason** to exactly: `Partial delivery — 10 units undelivered`
   - Change the **Credit Note Date** to **2026-04-30**
   - Click **Reverse** (or **Create Credit Note**)
4. You are now viewing the draft credit note. It will have the full 18 units.
   **Edit the quantity** on the credit note line from 18 to **10**.
5. Click **Confirm** to post the credit note.

After completing these steps, the credit note should be posted with quantity 10 and the original invoice should show a partial payment status.

**Rules:**
- Only create a credit note for CN-TARGET-01 (Lakeview Partners)
- The credit note must have quantity 10 (not the full 18)
- The credit note date must be 2026-04-30
- The reason must be exactly "Partial delivery — 10 units undelivered"
- Do not modify or interact with the CN-IGNORE-01 invoice
- Do not delete or cancel any invoices
