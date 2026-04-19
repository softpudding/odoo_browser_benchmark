"""Cleanup for account.reconcile_bank_statement_line_to_invoice.

BLOCKED TASK — required module is not available in this checkout.
Cleanup is a no-op to avoid NameError on missing models.
"""


def cleanup(env):
    accountant_mod = env["ir.module.module"].search(
        [("name", "=", "account_accountant")], limit=1
    )
    if not accountant_mod or accountant_mod.state != "installed":
        return
    # Once account_accountant is installed, cleanup should:
    #  - undo reconciliation on any 'BENCH-BANK-REC' statement line
    #    (stl.action_undo_reconciliation()), then delete the line
    #  - delete the seeded draft account.bank.statement
    #  - cancel + unlink the seeded 'BENCH-BANK-REC-001' invoice
    #  - remove the 'Bench Bank Cust' partner and 'Bench Bank Service'
    #    product if no other references remain
