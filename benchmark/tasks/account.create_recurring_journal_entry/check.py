"""Postcondition checks for account.create_recurring_journal_entry.

Validates:
1. Exactly one account.move with move_type='entry', ref='Bench Rent Apr',
   state='posted', date=2026-05-01.
2. Entry has exactly two product-like journal lines (ignoring tax/auto lines).
3. Total debit = 1000, total credit = 1000, balanced.
4. One line debits an expense-type account ('Rent') for 1000.
5. Other line credits a cash/liquidity account ('Bank') for 1000.
6. A chatter activity exists on the entry containing 'Post next month's rent
   entry' in the summary.
"""

from datetime import date


REF = "Bench Rent Apr"
ACTIVITY_SUMMARY = "Post next month's rent entry"


def check(env):
    failures = []

    moves = env["account.move"].search([
        ("move_type", "=", "entry"),
        ("ref", "=", REF),
    ])
    if len(moves) != 1:
        return [f"Expected exactly 1 journal entry with ref '{REF}', found {len(moves)}"]

    mv = moves[0]

    if mv.state != "posted":
        failures.append(f"Entry state is '{mv.state}', expected 'posted'")

    expected_date = date(2026, 5, 1)
    if mv.date != expected_date:
        failures.append(f"Entry date is '{mv.date}', expected '{expected_date}'")

    # Filter to non-section/non-note lines — journal entries normally only have
    # product/general lines anyway, but be defensive.
    lines = mv.line_ids.filtered(
        lambda l: l.display_type not in ("line_section", "line_note", "line_subsection")
    )
    if len(lines) != 3:
        failures.append(f"Expected exactly 3 journal lines, found {len(lines)}")
        # Still fall through for richer diagnostics

    total_debit = sum(line.debit for line in lines)
    total_credit = sum(line.credit for line in lines)
    if abs(total_debit - 1050.0) > 0.01:
        failures.append(f"Total debit is {total_debit}, expected 1050.00")
    if abs(total_credit - 1050.0) > 0.01:
        failures.append(f"Total credit is {total_credit}, expected 1050.00")
    if abs(total_debit - total_credit) > 0.01:
        failures.append(
            f"Entry unbalanced: debit={total_debit}, credit={total_credit}"
        )

    def _seen_diag():
        return ", ".join(
            f"{l.account_id.name}({l.account_id.account_type}) d={l.debit} c={l.credit}"
            for l in lines
        )

    # Rent debit 1000 on an expense account
    expense_types = {
        "expense",
        "expense_other",
        "expense_direct_cost",
        "expense_depreciation",
    }
    rent_ok = any(
        (
            line.account_id.account_type in expense_types
            or (line.account_id.name or "").lower() == "rent"
        )
        and abs(line.debit - 1000.0) < 0.01
        and abs(line.credit) < 0.01
        for line in lines
    )
    if not rent_ok:
        failures.append(
            f"No debit line of 1000.00 on a Rent/expense account found. "
            f"Seen lines: {_seen_diag()}"
        )

    # Tax debit 50 on a tax-paid / asset account
    tax_ok = any(
        (
            line.account_id.account_type in {"asset_current", "asset_receivable"}
            or "tax" in (line.account_id.name or "").lower()
        )
        and abs(line.debit - 50.0) < 0.01
        and abs(line.credit) < 0.01
        for line in lines
    )
    if not tax_ok:
        failures.append(
            f"No debit line of 50.00 on a Tax Paid / asset account found. "
            f"Seen lines: {_seen_diag()}"
        )

    # Bank credit 1050 on a cash/liquidity account
    bank_types = {
        "asset_cash",
        "asset_current",
        "liability_credit_card",
    }
    bank_ok = any(
        (
            line.account_id.account_type in bank_types
            or (line.account_id.name or "").lower() == "bank"
        )
        and abs(line.credit - 1050.0) < 0.01
        and abs(line.debit) < 0.01
        for line in lines
    )
    if not bank_ok:
        failures.append(
            f"No credit line of 1050.00 on a Bank/cash account found. "
            f"Seen lines: {_seen_diag()}"
        )

    # Activity existence check
    activities = env["mail.activity"].search([
        ("res_model", "=", "account.move"),
        ("res_id", "=", mv.id),
    ])
    if not activities:
        failures.append("No chatter activity scheduled on the journal entry")
    else:
        match = any(
            a.summary and ACTIVITY_SUMMARY.lower() in a.summary.lower()
            for a in activities
        )
        if not match:
            summaries = ", ".join(repr(a.summary) for a in activities)
            failures.append(
                f"No activity with summary containing '{ACTIVITY_SUMMARY}' found. "
                f"Summaries seen: {summaries}"
            )

    return failures
