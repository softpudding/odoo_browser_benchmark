"""Postcondition checks for account.create_manual_journal_entry_balanced.

Validates:
1. Exactly one account.move with move_type='entry', ref='Bench Manual Adj
   2026-04', state='posted', date=2026-04-30.
2. Entry is booked in a journal of type 'general' (Miscellaneous Operations).
3. Entry has exactly three journal item lines (ignoring section/note lines).
4. Total debit = total credit = 100.00 (balanced).
5. One debit line of 100.00 on an `asset_receivable` account, partner =
   'Bench Entity'.
6. Two credit lines on income accounts totalling 100.00, with one of
   60.00 and one of 40.00.
"""

from datetime import date


REF = "Bench Manual Adj 2026-04"
PARTNER_NAME = "Bench Entity"


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

    expected_date = date(2026, 4, 30)
    if mv.date != expected_date:
        failures.append(f"Entry date is '{mv.date}', expected '{expected_date}'")

    if mv.journal_id.type != "general":
        failures.append(
            f"Entry journal type is '{mv.journal_id.type}', expected 'general' "
            f"(Miscellaneous Operations). Journal: {mv.journal_id.name}"
        )

    lines = mv.line_ids.filtered(
        lambda l: l.display_type not in ("line_section", "line_note", "line_subsection")
    )
    if len(lines) != 3:
        failures.append(f"Expected exactly 3 journal lines, found {len(lines)}")

    total_debit = sum(line.debit for line in lines)
    total_credit = sum(line.credit for line in lines)
    if abs(total_debit - 100.0) > 0.01:
        failures.append(f"Total debit is {total_debit}, expected 100.00")
    if abs(total_credit - 100.0) > 0.01:
        failures.append(f"Total credit is {total_credit}, expected 100.00")
    if abs(total_debit - total_credit) > 0.01:
        failures.append(
            f"Entry unbalanced: debit={total_debit}, credit={total_credit}"
        )

    def _seen_diag():
        return ", ".join(
            f"{l.account_id.name}({l.account_id.account_type}) "
            f"d={l.debit} c={l.credit} partner={l.partner_id.name!r}"
            for l in lines
        )

    # Receivable debit 100 with Bench Entity partner
    receivable_lines = [
        l for l in lines
        if l.account_id.account_type == "asset_receivable"
        and abs(l.debit - 100.0) < 0.01
        and abs(l.credit) < 0.01
    ]
    if not receivable_lines:
        failures.append(
            f"No debit line of 100.00 on an asset_receivable account. "
            f"Seen lines: {_seen_diag()}"
        )
    else:
        r = receivable_lines[0]
        if not r.partner_id or r.partner_id.name != PARTNER_NAME:
            failures.append(
                f"Receivable line partner is {r.partner_id.name!r}, "
                f"expected {PARTNER_NAME!r}"
            )

    # Two income credit lines summing to 100 with amounts 60 and 40
    income_credit_lines = [
        l for l in lines
        if l.account_id.account_type == "income"
        and abs(l.debit) < 0.01
        and l.credit > 0.0
    ]
    if len(income_credit_lines) != 2:
        failures.append(
            f"Expected exactly 2 credit lines on income accounts, "
            f"found {len(income_credit_lines)}. Seen lines: {_seen_diag()}"
        )
    else:
        credits_set = sorted(round(l.credit, 2) for l in income_credit_lines)
        if credits_set != [40.0, 60.0]:
            failures.append(
                f"Income credit line amounts are {credits_set}, "
                f"expected [40.0, 60.0]"
            )
        # Must be two distinct income accounts (not the same one twice)
        distinct_accounts = {l.account_id.id for l in income_credit_lines}
        if len(distinct_accounts) != 2:
            failures.append(
                "The two income credit lines must use two different "
                "income accounts"
            )

    return failures
