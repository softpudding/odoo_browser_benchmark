"""Seed for account.create_manual_journal_entry_balanced.

Category: deep UI interaction (HARD).
The agent must navigate to Accounting -> Journal Entries (NOT Customer
Invoices), open the move_type='entry' form, select the Miscellaneous
Operations journal, and create a balanced THREE-line manual journal entry
with explicit Debit/Credit columns:

    - 100.00 debit on a receivable account for partner "Bench Entity"
    - 60.00 credit on a revenue (income) account
    - 40.00 credit on a second revenue (income) account

and finally post the entry. The three lines must balance.

The seed cleans up prior runs, creates the Bench Entity partner, ensures
one receivable account ("Bench Receivable") and two income accounts
("Bench Sales Revenue", "Bench Other Revenue") exist, and ensures a
Miscellaneous Operations general journal is visible under that exact name.
"""

REF = "Bench Manual Adj 2026-04"
PARTNER_NAME = "Bench Entity"
RECEIVABLE_NAME = "Bench Receivable"
RECEIVABLE_CODE = "121010"
SALES_NAME = "Bench Sales Revenue"
SALES_CODE = "700010"
OTHER_NAME = "Bench Other Revenue"
OTHER_CODE = "700020"


def _cleanup(env):
    # Delete any previous run's manual journal entry with our reference.
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


def _ensure_partner(env):
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if partner:
        return partner
    return env["res.partner"].create({
        "name": PARTNER_NAME,
        "company_type": "company",
    })


def _ensure_account(env, *, name, code, account_type):
    acc = env["account.account"].search([
        ("name", "=", name),
        ("account_type", "=", account_type),
    ], limit=1)
    if acc:
        return acc
    # If an account with the desired code already exists, normalise its
    # name/type; otherwise create it fresh.
    existing = env["account.account"].search([("code", "=", code)], limit=1)
    if existing:
        vals = {}
        if existing.name != name:
            vals["name"] = name
        if existing.account_type != account_type:
            vals["account_type"] = account_type
        if vals:
            existing.write(vals)
        return existing
    return env["account.account"].create({
        "name": name,
        "code": code,
        "account_type": account_type,
    })


def _ensure_misc_journal(env):
    misc = env["account.journal"].search([
        ("type", "=", "general"),
        ("name", "=", "Miscellaneous Operations"),
    ], limit=1)
    if misc:
        return misc
    # Try the conventional Odoo 19 xmlid for the Miscellaneous journal.
    try:
        ref = env.ref("account.1_miscellaneous_journal_active")
        if ref and ref.type == "general":
            if ref.name != "Miscellaneous Operations":
                ref.name = "Miscellaneous Operations"
            return ref
    except Exception:
        pass
    # Fallback: rename any existing general journal.
    generic = env["account.journal"].search([("type", "=", "general")], limit=1)
    if generic:
        if generic.name != "Miscellaneous Operations":
            generic.name = "Miscellaneous Operations"
        return generic
    return env["account.journal"].create({
        "name": "Miscellaneous Operations",
        "code": "MISC",
        "type": "general",
    })


def setup(env):
    _cleanup(env)

    _ensure_partner(env)

    _ensure_account(env,
        name=RECEIVABLE_NAME,
        code=RECEIVABLE_CODE,
        account_type="asset_receivable",
    )
    _ensure_account(env,
        name=SALES_NAME,
        code=SALES_CODE,
        account_type="income",
    )
    _ensure_account(env,
        name=OTHER_NAME,
        code=OTHER_CODE,
        account_type="income",
    )

    _ensure_misc_journal(env)

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
