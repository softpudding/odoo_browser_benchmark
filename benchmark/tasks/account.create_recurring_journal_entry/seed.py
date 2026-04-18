"""Seed for account.create_recurring_journal_entry.

Category 5 (HARD): Deep UI interaction.
Force the agent to navigate to Accounting -> Journal Entries (NOT Customer
Invoices), open the move_type='entry' form (different from invoice form),
create a balanced THREE-line entry with explicit Debit/Credit columns, schedule
a chatter activity for monthly reminder, and post the entry.

The seed cleans up prior runs, ensures Rent / Tax Paid / Bank accounts exist
with deterministic names, and grants admin the accountant groups so the
Journal Items tab renders. The base snapshot (l10n_generic_coa) ships:
    - "Rent" (code 6120, account_type='expense')
    - "Tax Paid" (code 1310, account_type='asset_current')
    - Bank journal auto-creates a liquidity account named "Bank"
If any are missing in an alternate base setup, they are created.
"""

REF = "Bench Rent Apr"


def _cleanup(env):
    # Delete any previous run's journal entry with our reference.
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

    # Delete any stray activity left behind by a prior run on a deleted move
    # (normally cascaded with the move, but guard for safety).
    leftover = env["mail.activity"].search([
        ("summary", "=", "Post next month's rent entry"),
        ("res_model", "=", "account.move"),
    ])
    leftover.unlink()


def _ensure_rent_account(env):
    """Return the Rent expense account (create if missing)."""
    acc = env["account.account"].search([
        ("name", "=", "Rent"),
        ("account_type", "=", "expense"),
    ], limit=1)
    if acc:
        return acc
    # Try by code 6120 (l10n_generic_coa default).
    acc = env["account.account"].search([("code", "=", "6120")], limit=1)
    if acc:
        # Normalise name to "Rent" for the prompt's autocomplete.
        if acc.name != "Rent":
            acc.name = "Rent"
        return acc
    # Fallback: create a Rent expense account.
    return env["account.account"].create({
        "name": "Rent",
        "code": "6120",
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
    # The default Bank journal's default_account_id is typically named Bank.
    bank_journal = env["account.journal"].search([
        ("type", "=", "bank"),
        ("name", "=", "Bank"),
    ], limit=1)
    if bank_journal and bank_journal.default_account_id:
        bank_journal.default_account_id.name = "Bank"
        return bank_journal.default_account_id
    # Fallback: any bank journal's default account.
    bank_journal = env["account.journal"].search([("type", "=", "bank")], limit=1)
    if bank_journal and bank_journal.default_account_id:
        if bank_journal.default_account_id.name != "Bank":
            bank_journal.default_account_id.name = "Bank"
        return bank_journal.default_account_id
    # Last-resort: create a Bank liquidity account.
    return env["account.account"].create({
        "name": "Bank",
        "code": "101401",
        "account_type": "asset_cash",
    })


def _ensure_tax_paid_account(env):
    acc = env["account.account"].search([
        ("name", "=", "Tax Paid"),
    ], limit=1)
    if acc:
        return acc
    acc = env["account.account"].search([("code", "=", "131000")], limit=1)
    if not acc:
        acc = env["account.account"].search([("code", "=", "1310")], limit=1)
    if acc:
        if acc.name != "Tax Paid":
            acc.name = "Tax Paid"
        return acc
    return env["account.account"].create({
        "name": "Tax Paid",
        "code": "131000",
        "account_type": "asset_current",
    })


def setup(env):
    _cleanup(env)
    _ensure_rent_account(env)
    _ensure_bank_account(env)
    _ensure_tax_paid_account(env)

    # Ensure the admin user has the accountant/readonly groups so the
    # Journal Items tab (groups="account.group_account_readonly") renders
    # on the entry form. Note: res.groups field is user_ids in Odoo 19.
    admin = env.ref("base.user_admin")
    for xmlid in (
        "account.group_account_readonly",
        "account.group_account_invoice",
        "account.group_account_user",
    ):
        grp = env.ref(xmlid, raise_if_not_found=False)
        if grp and admin not in grp.user_ids:
            grp.sudo().write({"user_ids": [(4, admin.id)]})

    # Ensure a Miscellaneous (general) journal exists and is visible by name.
    misc = env["account.journal"].search([
        ("type", "=", "general"),
        ("name", "=", "Miscellaneous Operations"),
    ], limit=1)
    if not misc:
        # A default "Miscellaneous" general journal is usually present; rename
        # it for deterministic autocomplete.
        generic = env["account.journal"].search([("type", "=", "general")], limit=1)
        if generic:
            generic.name = "Miscellaneous Operations"
