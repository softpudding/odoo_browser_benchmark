# Reconcile a bank statement line to a posted invoice (BLOCKED)

> **Note**: This task is BLOCKED in the Odoo 19 Community Edition checkout
> used for this benchmark. The required "Accounting → Bank →
> open statement → select line → pick matching invoice → **Validate**"
> workflow runs inside the Enterprise-only `bank.rec.widget` shipped with
> the `account_accountant` addon, whose source is not vendored under
> `addons/` in this checkout.
>
> Community's bare `account` addon exposes `account.bank.statement` +
> `account.bank.statement.line` records but has no dedicated two-panel
> bank-reconciliation widget, no `action_open_bank_reconcile_widget`
> action, and no `Validate` button on statement lines. Any "reconcile"
> flow in Community has to edit the statement line's counterpart
> `account.move.line` (repoint it to the invoice's receivable account)
> and call `account.move.line.reconcile()` directly — which is the flow
> already captured by row 211
> (`account.reconcile_bank_statement_line_manual`) and is NOT the same
> capability as the Enterprise widget this task was designed to probe.
>
> The original task intent is preserved below for future re-scoping when
> `account_accountant` is vendored and added to `base_modules.txt`.

You will reconcile a seeded bank statement line against a posted customer
invoice using the Enterprise bank reconciliation widget.

## Context

- Customer: **Bench Bank Cust**
- Posted customer invoice `BENCH-BANK-REC-001`, total **€300.00**, in
  state **Not Paid**.
- A draft `account.bank.statement` with one unreconciled statement line
  for `partner_id = Bench Bank Cust`, `amount = 300.00`.

## Steps

1. Open **Accounting → Bank** (or **Accounting → Reconciliation**).
2. Open the seeded draft statement and select the `BENCH-BANK-REC` line.
3. In the reconciliation widget, pick the matching posted invoice
   `BENCH-BANK-REC-001` from the suggested/open invoice list.
4. Click **Validate** to commit the reconciliation.

## Rules

- After validation, `invoice.payment_state` must be `'paid'`.
- The bank statement line must have `reconciled_ids` linking to the
  invoice's receivable move lines (`is_reconciled = True`,
  `amount_residual = 0.0`).
- Do NOT use the invoice's **Register Payment** wizard (distinct from
  row 416 "direct payment") and do NOT open the partial-payment wizard
  (distinct from row 435). This task specifically exercises the bank
  reconciliation widget + Validate.
