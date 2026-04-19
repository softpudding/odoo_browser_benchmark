# Reconcile Bank Statement Line Against Customer Invoice

A customer has paid a posted invoice. You must manually reconcile the
corresponding **bank statement line** against the **open customer invoice**
so the invoice becomes fully paid.

## Context

- Customer: **Bench Reconcile Customer**
- Posted customer invoice total: **€500.00**, reference `BENCH-RECO-01`,
  currently in state **Not Paid** (no payment yet registered).
- A bank statement line exists in the **Bank** journal for this customer:
  - Label / Memo: `Bench Reconcile 500`
  - Amount: `500.00`
  - Currently **not reconciled** (appears in the bank reconciliation view
    with a red/unreconciled status).

## Steps

1. Open the **Accounting** app.
2. Navigate to **Accounting → Journal Entries → Bank Statement Lines**
   (or the Bank journal's transactions list). Find the unreconciled line
   with label `Bench Reconcile 500` for `Bench Reconcile Customer`.
3. Open / select that bank statement line so you can edit its
   reconciliation. In the reconciliation view, the right-hand panel shows
   suggested matches / open customer invoices.
4. **Manually select** the open posted customer invoice for
   `Bench Reconcile Customer` (amount €500.00). Do NOT rely on any
   auto-match suggestion — pick this specific invoice by clicking it in
   the list of matching open invoices.
5. **Validate** the reconciliation (the Validate / Save button in the
   reconciliation widget). After validation:
   - The bank statement line's status changes to **Matched / Reconciled**.
   - The customer invoice's payment status becomes **Paid** (amount due =
     `0.00`).

## Rules

- You must reconcile the statement line against the **existing open
  invoice** for `Bench Reconcile Customer`. Do NOT create a new payment
  via the "Register Payment" wizard on the invoice and do NOT create a
  new journal entry.
- The invoice's payment state after your work must be **Paid**.
- The bank statement line must end up fully reconciled
  (`is_reconciled = True`, `amount_residual = 0.0`).
- Do NOT modify the invoice's lines, date, or amount.
- Do NOT reconcile a different customer's bank line or invoice.
