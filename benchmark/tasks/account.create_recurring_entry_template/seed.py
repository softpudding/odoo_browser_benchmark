"""Seed for account.create_recurring_entry_template.

Category: deep UI interaction (medium).
The agent must open a draft journal entry (move_type='entry'), navigate to
the Other Info tab, change the Auto-post selection from No to Monthly, and
fill the conditionally-rendered Auto-post until date. The entry must stay in
draft state at the end (no Post).

Pre-requisites already proven by the sibling
`account.create_recurring_journal_entry` seed:

- l10n_generic_coa ships an "Office Supplies" expense account (code 6510).
- Default bank journal auto-creates a liquidity account; we rename to "Bank".
- Admin needs `account.group_account_readonly/invoice/user` so the Journal
  Items tab renders on the entry form.
"""

REF = "Bench Office Supplies Tmpl"


def _cleanup(env):
    moves = env["account.move"].search([
        ("move_type", "=", "entry"),
        ("ref", "=", REF),
    ])
    for mv in moves:
        if mv.state == "posted":
            mv.button_draft()
        if mv.state != "cancel":
            try:
                mv.button_cancel()
            except Exception:
                pass
        mv.unlink()


def _ensure_office_supplies_account(env):
    """Return an expense account named exactly 'Office Supplies'."""
    acc = env["account.account"].search([
        ("name", "=", "Office Supplies"),
        ("account_type", "=", "expense"),
    ], limit=1)
    if acc:
        return acc
    # l10n_generic_coa uses code 6510 for office supplies.
    acc = env["account.account"].search([("code", "=", "6510")], limit=1)
    if acc:
        if acc.name != "Office Supplies":
            acc.name = "Office Supplies"
        return acc
    return env["account.account"].create({
        "name": "Office Supplies",
        "code": "6510",
        "account_type": "expense",
    })


def _ensure_bank_account(env):
    """Return a liquidity account named exactly 'Bank'."""
    acc = env["account.account"].search([
        ("name", "=", "Bank"),
        ("account_type", "in", ["asset_cash", "asset_current"]),
    ], limit=1)
    if acc:
        return acc
    bank_journal = env["account.journal"].search([
        ("type", "=", "bank"),
        ("name", "=", "Bank"),
    ], limit=1)
    if bank_journal and bank_journal.default_account_id:
        bank_journal.default_account_id.name = "Bank"
        return bank_journal.default_account_id
    bank_journal = env["account.journal"].search([("type", "=", "bank")], limit=1)
    if bank_journal and bank_journal.default_account_id:
        if bank_journal.default_account_id.name != "Bank":
            bank_journal.default_account_id.name = "Bank"
        return bank_journal.default_account_id
    return env["account.account"].create({
        "name": "Bank",
        "code": "101402",
        "account_type": "asset_cash",
    })


def _ensure_misc_journal(env):
    misc = env["account.journal"].search([
        ("type", "=", "general"),
        ("name", "=", "Miscellaneous Operations"),
    ], limit=1)
    if misc:
        return misc
    generic = env["account.journal"].search([("type", "=", "general")], limit=1)
    if generic:
        generic.name = "Miscellaneous Operations"
        return generic
    return env["account.journal"].create({
        "name": "Miscellaneous Operations",
        "code": "MISC",
        "type": "general",
    })


def setup(env):
    _cleanup(env)

    rent = _ensure_office_supplies_account(env)
    bank = _ensure_bank_account(env)
    misc = _ensure_misc_journal(env)

    # Ensure the admin user has the accountant/readonly groups so the
    # Journal Items tab (groups="account.group_account_readonly") renders
    # on the entry form.
    admin = env.ref("base.user_admin")
    for xmlid in (
        "account.group_account_readonly",
        "account.group_account_invoice",
        "account.group_account_user",
    ):
        grp = env.ref(xmlid, raise_if_not_found=False)
        if grp and admin not in grp.user_ids:
            grp.sudo().write({"user_ids": [(4, admin.id)]})

    # Create the draft journal entry. auto_post defaults to 'no'.
    env["account.move"].create({
        "move_type": "entry",
        "ref": REF,
        "date": "2026-05-01",
        "journal_id": misc.id,
        "line_ids": [
            (0, 0, {
                "account_id": rent.id,
                "name": "Monthly office supplies accrual",
                "debit": 500.00,
                "credit": 0.00,
            }),
            (0, 0, {
                "account_id": bank.id,
                "name": "Monthly office supplies payment",
                "debit": 0.00,
                "credit": 500.00,
            }),
        ],
    })
