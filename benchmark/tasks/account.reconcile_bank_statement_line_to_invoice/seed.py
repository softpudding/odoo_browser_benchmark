"""Seed for account.reconcile_bank_statement_line_to_invoice.

BLOCKED TASK — the Enterprise-only `account_accountant` addon (which
provides the `bank.rec.widget` reconciliation UI required by this task)
is not vendored under `addons/` in this Odoo 19 Community checkout.

The Community `account` addon ships `account.bank.statement` +
`account.bank.statement.line` records, but it does NOT ship the
two-panel bank reconciliation widget / `Validate` action. Any direct
reconcile has to be performed by editing the statement line's
counterpart `account.move.line` and calling `reconcile()` — which is
the flow already exercised by row 211
(`account.reconcile_bank_statement_line_manual`), not the widget flow
this task is intended to probe.

This seed raises a clear error so the eval pipeline records the blocker
instead of silently crashing inside the browser phase.
"""


def setup(env):
    accountant_mod = env["ir.module.module"].search(
        [("name", "=", "account_accountant")], limit=1
    )
    if not accountant_mod or accountant_mod.state == "uninstallable":
        raise RuntimeError(
            "BLOCKED: account_accountant (Enterprise-only) is not "
            "available in this Odoo 19 Community checkout. The bank "
            "reconciliation widget (`bank.rec.widget` + the Validate "
            "flow on `account.bank.statement.line`) requires this "
            "addon. See STATUS.md row 455 for details."
        )
    if accountant_mod.state != "installed":
        raise RuntimeError(
            "BLOCKED: account_accountant is present but not installed "
            "in benchmark_base. Add `account_accountant` to "
            "benchmark/base_modules.txt and rebuild the snapshot before "
            "unblocking this task. See STATUS.md row 455 for details."
        )

    # Concrete seed body to add when account_accountant is available:
    #  1. Ensure partner `Bench Bank Cust` exists.
    #  2. Create a service product `Bench Bank Service` priced 300.00,
    #     tax_ids cleared.
    #  3. Create + post an `account.move` (out_invoice) with ref
    #     'BENCH-BANK-REC-001', partner=Bench Bank Cust, one line
    #     qty=1 price_unit=300.00 — verify payment_state='not_paid'.
    #  4. Resolve the default bank journal; create a DRAFT
    #     `account.bank.statement` on that journal with one
    #     `account.bank.statement.line`: payment_ref='BENCH-BANK-REC',
    #     partner_id=Bench Bank Cust, amount=300.00, date today.
    #  5. Make sure admin is in `account.group_account_user` so the
    #     reconciliation widget renders.
    raise NotImplementedError(
        "Seed body intentionally left empty — flesh out when "
        "account_accountant (Enterprise) is vendored and installed in "
        "the base snapshot."
    )
