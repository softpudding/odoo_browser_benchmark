"""Oracle for account.reconcile_bank_statement_line_to_invoice.

BLOCKED TASK — the Enterprise-only `account_accountant` addon, which
provides the `bank.rec.widget` reconciliation UI and the Validate
button on `account.bank.statement.line`, is not vendored in this Odoo
19 Community checkout. The oracle exits with a clear error so the
harness records the blocker instead of producing spurious results.

To flesh out once `account_accountant` is available:
  1. Open /odoo/action-account_accountant.action_bank_reconcile_widget
     (or Accounting → Bank → <BankJournal> → Reconcile).
  2. Select the seeded draft statement, click the BENCH-BANK-REC line.
  3. In the right-hand panel, pick `BENCH-BANK-REC-001` from Suggested
     / Customer Invoices tab.
  4. Click Validate.
  5. Assert invoice.payment_state='paid' and statement_line.is_reconciled.

If the widget proves too fragile for a deterministic Playwright oracle,
fall back to JSON-RPC: draft the statement line move, repoint its
counterpart `account.move.line` to the invoice's receivable account,
re-post, and call `account.move.line.reconcile([invRecv.id, stlCounter.id])`
— same shape as row 211's oracle.
"""

from benchmark.oracle_helpers import run_oracle


def oracle(page):
    raise RuntimeError(
        "BLOCKED: account_accountant is Enterprise-only and absent "
        "from this Odoo Community checkout; the bank reconciliation "
        "widget + Validate flow cannot be exercised. Oracle body "
        "intentionally short-circuits. See STATUS.md row 455."
    )


run_oracle(oracle)
