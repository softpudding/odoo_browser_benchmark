"""Seed for account.import_opening_balance_set_initial_equity.

Category 5 (HARD): Deep UI interaction.
The agent must create an **opening balance** journal entry from scratch in the
Miscellaneous Operations journal (move_type='entry', NOT an invoice). Two
balanced lines must be entered via the Journal Items one2many:
  * Debit 10000.00 -> `Stock Valuation` (asset_current, code 140000)
  * Credit 10000.00 -> `Opening Balance` (equity)

The seed ensures:
  * Admin user has the accountant readonly/invoice/user groups so the Journal
    Items tab (groups="account.group_account_readonly") renders on the entry
    form.
  * A general journal named exactly "Miscellaneous Operations" exists.
  * A `Stock Valuation` asset account (code 140000) exists (generic l10n CoA
    has no such account — manufacturing/stock_account tasks seed it; we
    create it defensively here).
  * A dedicated `Opening Balance` equity account exists so the credit-side
    autocomplete is deterministic.
  * No prior run of this task is still present (cleanup by ref).
"""

REF = "OPEN-BAL-001"
EQUITY_ACCOUNT_NAME = "Opening Balance"
EQUITY_ACCOUNT_CODE = "300100"
STOCK_ACCOUNT_NAME = "Stock Valuation"
STOCK_ACCOUNT_CODE = "140000"


def _cleanup(env):
    moves = env["account.move"].search([
        ("move_type", "=", "entry"),
        ("ref", "=", REF),
    ])
    for mv in moves:
        if mv.state == "posted":
            try:
                mv.button_draft()
            except Exception:
                pass
        if mv.state != "cancel":
            try:
                mv.button_cancel()
            except Exception:
                pass
        try:
            mv.unlink()
        except Exception:
            pass


def _ensure_stock_valuation_account(env):
    """Ensure a `Stock Valuation` asset account (code 140000) exists."""
    acc = env["account.account"].search([
        ("name", "=", STOCK_ACCOUNT_NAME),
        ("code", "=", STOCK_ACCOUNT_CODE),
    ], limit=1)
    if acc:
        return acc
    # Try by code alone — if a 140000 account exists under a different name
    # (unlikely in generic_coa), rename for deterministic autocomplete.
    acc = env["account.account"].search([
        ("code", "=", STOCK_ACCOUNT_CODE),
    ], limit=1)
    if acc:
        if acc.name != STOCK_ACCOUNT_NAME:
            acc.name = STOCK_ACCOUNT_NAME
        return acc
    # Or by name alone on any asset_current account.
    acc = env["account.account"].search([
        ("name", "=", STOCK_ACCOUNT_NAME),
    ], limit=1)
    if acc:
        # Normalise code if missing.
        if not acc.code:
            acc.code = STOCK_ACCOUNT_CODE
        return acc
    return env["account.account"].create({
        "name": STOCK_ACCOUNT_NAME,
        "code": STOCK_ACCOUNT_CODE,
        "account_type": "asset_current",
    })


def _ensure_opening_balance_account(env):
    """Ensure an `Opening Balance` equity account exists."""
    acc = env["account.account"].search([
        ("name", "=", EQUITY_ACCOUNT_NAME),
        ("account_type", "=", "equity"),
    ], limit=1)
    if acc:
        return acc
    # Avoid colliding with any existing 300100 code.
    acc = env["account.account"].search([
        ("code", "=", EQUITY_ACCOUNT_CODE),
    ], limit=1)
    if acc:
        if acc.name != EQUITY_ACCOUNT_NAME:
            acc.name = EQUITY_ACCOUNT_NAME
        if acc.account_type != "equity":
            acc.account_type = "equity"
        return acc
    return env["account.account"].create({
        "name": EQUITY_ACCOUNT_NAME,
        "code": EQUITY_ACCOUNT_CODE,
        "account_type": "equity",
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

    _ensure_stock_valuation_account(env)
    _ensure_opening_balance_account(env)
    _ensure_misc_journal(env)

    # Ensure admin user has the accountant/readonly groups so the Journal Items
    # tab (groups="account.group_account_readonly") renders on the entry form.
    admin = env.ref("base.user_admin")
    for xmlid in (
        "account.group_account_readonly",
        "account.group_account_invoice",
        "account.group_account_user",
    ):
        grp = env.ref(xmlid, raise_if_not_found=False)
        if grp and admin not in grp.user_ids:
            grp.sudo().write({"user_ids": [(4, admin.id)]})
