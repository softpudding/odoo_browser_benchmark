Open the Invoicing (Accounting) app. There is one **posted, unpaid** customer invoice:

| Customer        | Reference         | Total   | Status                 |
|-----------------|-------------------|---------|------------------------|
| Bench Recon Co  | INV/BENCH/RECON   | 500.00  | Posted / Not Paid      |

The customer has sent you a full bank payment of `500.00` for this invoice.
You need to register that payment against this exact invoice so it gets
reconciled (payment state should become `Paid` or `In Payment`).

Your job:

1. Open the posted invoice whose **Customer Reference** is `INV/BENCH/RECON`
   (customer: `Bench Recon Co`).
2. In the invoice header, click the **Pay** button (this is the Register
   Payment action). It opens the `Register Payment` wizard.
3. In the wizard:
   - **Journal** must be `Bank` (not `Cash`).
   - **Payment Method** must be `Manual`.
   - **Amount** must be `500.00` (leave the default, which is the invoice total).
   - **Payment Date** must be today's date (leave the default).
   - Leave the **Memo** at its default value (it references the invoice).
4. Click the primary **Create Payment** button in the wizard footer. Do **not**
   click **Discard**.
5. Posting the payment through the wizard will automatically post the
   `account.payment` and reconcile it against the invoice.

**Rules:**
- The invoice `INV/BENCH/RECON` must remain `Posted` and must end up with
  `payment_state` equal to `paid` or `in_payment` (both mean the payment
  is reconciled).
- Exactly **one** `account.payment` for `Bench Recon Co` must be created,
  with `amount = 500.00`, `state = posted`, and `partner_id = Bench Recon Co`.
- Do NOT reset the invoice to draft, cancel it, or edit its lines.
- Do NOT create a credit note or any second payment.
- Use the `Bank` journal with the `Manual` payment method — do NOT pick Cash
  or any other journal.
