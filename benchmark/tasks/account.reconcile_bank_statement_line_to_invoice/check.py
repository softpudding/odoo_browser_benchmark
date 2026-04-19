"""Postcondition checks for account.reconcile_bank_statement_line_to_invoice.

BLOCKED TASK — account_accountant (Enterprise-only) is not available
in this checkout, so the bank reconciliation widget + Validate flow
cannot run end-to-end. The check below returns a clear failure so the
eval pipeline flags it rather than appearing as a spurious PASS.
"""


def check(env):
    accountant_mod = env["ir.module.module"].search(
        [("name", "=", "account_accountant")], limit=1
    )
    if not accountant_mod or accountant_mod.state == "uninstallable":
        return [
            "BLOCKED: account_accountant (Enterprise-only) is "
            "uninstallable in this Odoo Community checkout — the bank "
            "reconciliation widget + Validate flow cannot be validated "
            "end-to-end."
        ]
    if accountant_mod.state != "installed":
        return [
            "BLOCKED: account_accountant is not installed in "
            "benchmark_base. Add it to benchmark/base_modules.txt "
            "before unblocking."
        ]

    # Concrete validation to add once the module is installed:
    #  - customer invoice with ref='BENCH-BANK-REC-001' exists, state='posted',
    #    payment_state='paid', amount_residual=0.0
    #  - account.bank.statement.line with label/payment_ref starting
    #    'BENCH-BANK-REC' is_reconciled=True, amount_residual=0.0
    #  - the statement line's counterpart move line shares its
    #    full_reconcile_id with the invoice's receivable move line
    #    (verify via account.full.reconcile membership)
    return [
        "BLOCKED: module was available but check body not yet "
        "implemented. See STATUS.md row 455 for context."
    ]
