Open the Invoicing (Accounting) app. Customer `Bench Partial Co` has TWO
posted customer invoices. You must register a **partial** bank payment
against ONE of them:

| Customer           | Reference              | Total   | Status              | Action required       |
|--------------------|------------------------|---------|---------------------|-----------------------|
| Bench Partial Co   | `BENCH-PARTIAL-001`    | 500.00  | Posted / Not Paid   | **Register 200.00 partial payment** |
| Bench Partial Co   | `BENCH-PARTIAL-DISTRACT` | 300.00 | Posted / Not Paid   | **DO NOT touch**      |

The customer has wired you only `200.00` so far against `BENCH-PARTIAL-001`.
You must record that partial receipt today against the correct invoice so
its `payment_state` becomes `Partial` (not `Paid`, not `In Payment`).

Your job:

1. Open **Accounting** → **Customers** → **Invoices**.
2. Open the posted invoice whose **Customer Reference** is
   `BENCH-PARTIAL-001` (customer: `Bench Partial Co`, total 500.00).
   Do NOT open `BENCH-PARTIAL-DISTRACT`.
3. In the invoice header, click the **Pay** button (this is the Register
   Payment action). A `Register Payment` modal wizard will appear.
4. The wizard auto-fills several fields; you MUST override FOUR of
   them and leave the rest at default:
   - **Amount**: wizard pre-fills with the full invoice total `500.00`.
     Change it to `200.00` (TRAP #1 — do not accept the default full
     amount).
   - **Journal**: wizard pre-fills with `Bench Secondary Bank` (a
     secondary bank journal that happens to be the default). Change
     the Journal dropdown to `Bank` (TRAP #2 — the default here is
     NOT the right journal).
   - **Memo**: wizard pre-fills with the invoice name (e.g.
     `INV/2026/00001`). Change it to exactly
     `Partial 1 of 2 for BENCH-PARTIAL-001` (TRAP #3 — do not leave
     the default).
   - **Payment Date**: wizard pre-fills with today's date. Back-date
     it to `04/15/2026` (TRAP #4 — the wire arrived four days ago
     and accounting wants the actual receipt date, not today).
   - **Payment Method**: leave the default (`Manual`).
5. Click the primary **Create Payment** button in the wizard footer. Do
   NOT click **Discard**.
6. Posting the payment through the wizard will automatically post the
   `account.payment` and partially reconcile it against the invoice.

**Rules:**
- Invoice `BENCH-PARTIAL-001` must remain `Posted` and must end up with
  `payment_state` equal to **`partial`** (meaning some but not all of the
  receivable is reconciled). It must NOT be `paid`, `in_payment`, or
  `not_paid`.
- Invoice `BENCH-PARTIAL-DISTRACT` must remain `Posted / Not Paid` and
  completely untouched.
- Exactly **one** `account.payment` for `Bench Partial Co` must be
  created, with `amount = 200.00`, `state` in (`posted`, `paid`,
  `in_process`), `payment_type = inbound`, `partner_id = Bench Partial
  Co`, `date = 2026-04-15`, and `memo = "Partial 1 of 2 for
  BENCH-PARTIAL-001"` (exact text, including the dash and
  capitalisation).
- Use the `Bank` journal with the `Manual` payment method. Do NOT use
  the default `Bench Secondary Bank` journal, do NOT pick `Cash`, and
  do NOT pick any other journal. The resulting `account.payment` must
  sit on a Bank-type journal whose name is exactly `Bank`.
- Do NOT reset either invoice to draft, cancel them, or edit their
  lines.
- Do NOT create a credit note, a second payment, or any refund.
