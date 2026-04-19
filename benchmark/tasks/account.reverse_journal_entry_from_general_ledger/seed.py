"""Seed a posted, balanced miscellaneous journal entry for the reversal task.

Category 5: Deep UI interaction.
The agent must navigate the grouped Miscellaneous Journal Items report
(not Customer Invoices, not the flat Journal Entries list) to drill into
the posted entry BENCH-GL-REV, open the `account.move` form, and click
the 'Reverse Entry' header button to open the account.move.reversal
wizard. The wizard has only Journal + Reversal Date (no Reason field for
move_type='entry') and a primary 'Reverse' button that creates and posts
a linked reversed entry with debit/credit swapped.

Seed cleans up prior runs, ensures Rent / Bank accounts with
deterministic names, ensures a Misc (general) journal named
'Miscellaneous Operations', and grants the admin user the accountant
readonly group so the Misc Journal Items report and Reverse Entry
button render.
"""

REF = "BENCH-GL-REV"


def _cleanup(env):
    # Sweep any prior runs of this task — unlink reversals first, then
    # the source entry(ies).
    old_moves = env["account.move"].search([("ref", "=", REF)])
    for mv in old_moves:
        reversals = env["account.move"].search([
            ("reversed_entry_id", "=", mv.id),
        ])
        for rev in reversals:
            if rev.state == "posted":
                try:
                    rev.button_draft()
                except Exception:
                    pass
            try:
                rev.button_cancel()
            except Exception:
                pass
            try:
                rev.unlink()
            except Exception:
                pass
        # Unreconcile the source entry lines in case a prior reversal
        # auto-reconciled them.
        for line in mv.line_ids.filtered(
            lambda l: l.matched_debit_ids or l.matched_credit_ids
        ):
            try:
                line.remove_move_reconcile()
            except Exception:
                pass
        if mv.state == "posted":
            try:
                mv.button_draft()
            except Exception:
                pass
        try:
            mv.button_cancel()
        except Exception:
            pass
        try:
            mv.unlink()
        except Exception:
            pass


def _ensure_rent_account(env):
    acc = env["account.account"].search([
        ("name", "=", "Rent"),
        ("account_type", "=", "expense"),
    ], limit=1)
    if acc:
        return acc
    acc = env["account.account"].search([("code", "=", "6120")], limit=1)
    if acc:
        if acc.name != "Rent":
            acc.name = "Rent"
        return acc
    return env["account.account"].create({
        "name": "Rent",
        "code": "6120",
        "account_type": "expense",
    })


def _ensure_bank_account(env):
    acc = env["account.account"].search([
        ("name", "=", "Bank"),
        ("account_type", "in", ["asset_cash", "asset_current"]),
    ], limit=1)
    if acc:
        return acc
    bank_journal = env["account.journal"].search([
        ("type", "=", "bank"),
    ], limit=1)
    if bank_journal and bank_journal.default_account_id:
        if bank_journal.default_account_id.name != "Bank":
            bank_journal.default_account_id.name = "Bank"
        return bank_journal.default_account_id
    return env["account.account"].create({
        "name": "Bank",
        "code": "101401",
        "account_type": "asset_cash",
    })


def _ensure_misc_journal(env):
    misc = env["account.journal"].search([
        ("type", "=", "general"),
        ("name", "=", "Miscellaneous Operations"),
    ], limit=1)
    if misc:
        return misc
    generic = env["account.journal"].search([
        ("type", "=", "general"),
    ], limit=1)
    if generic:
        if generic.name != "Miscellaneous Operations":
            generic.name = "Miscellaneous Operations"
        return generic
    return env["account.journal"].create({
        "name": "Miscellaneous Operations",
        "type": "general",
        "code": "MISC",
    })


def setup(env):
    _cleanup(env)
    rent = _ensure_rent_account(env)
    bank = _ensure_bank_account(env)
    misc = _ensure_misc_journal(env)

    # Grant admin the accountant readonly/user groups so the Miscellaneous
    # Journal Items report and the Reverse Entry header button render.
    admin = env.ref("base.user_admin")
    for xmlid in (
        "account.group_account_readonly",
        "account.group_account_invoice",
        "account.group_account_user",
    ):
        grp = env.ref(xmlid, raise_if_not_found=False)
        if grp and admin not in grp.user_ids:
            grp.sudo().write({"user_ids": [(4, admin.id)]})

    # Create the balanced entry.
    move = env["account.move"].create({
        "move_type": "entry",
        "journal_id": misc.id,
        "ref": REF,
        "date": "2026-04-15",
        "line_ids": [
            (0, 0, {
                "account_id": rent.id,
                "name": "Rent line",
                "debit": 100.0,
                "credit": 0.0,
            }),
            (0, 0, {
                "account_id": bank.id,
                "name": "Bank line",
                "debit": 0.0,
                "credit": 100.0,
            }),
        ],
    })
    move.action_post()
