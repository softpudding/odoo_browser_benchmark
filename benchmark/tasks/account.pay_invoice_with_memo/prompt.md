Go to the **Invoicing** app (or Accounting app).

Find the posted customer invoice with reference **BENCH-PAYMEMO-01** for customer **"Highfield Consulting"**. The invoice amount is **$2,400.00**.

Register a payment on this invoice:

1. Click the **Pay** button on the invoice.
2. In the **Register Payment** dialog:
   - Change the **Memo** field to: `Q2-2026-INV-SETTLE`
   - Change the **Payment Date** to: `05/08/2026`
   - Keep all other fields at their defaults (do not change journal, amount, or currency).
3. Click **Create Payment**.

**Rules:**
- Only pay invoice BENCH-PAYMEMO-01 — do not pay any other invoices
- Do not change the payment amount ($2,400.00)
- Do not change the payment journal
- Set the Memo to exactly `Q2-2026-INV-SETTLE` (case-sensitive)
- Set the Payment Date to May 8, 2026 only
