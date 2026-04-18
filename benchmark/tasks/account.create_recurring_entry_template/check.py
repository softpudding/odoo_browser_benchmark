"""Postcondition checks for account.create_recurring_entry_template.

Validates:
1. Exactly one draft account.move with move_type='entry',
   ref='Bench Office Supplies Tmpl'.
2. auto_post == 'monthly'.
3. auto_post_until == 2026-08-01.
4. State is still 'draft' (task forbids posting).
5. Underlying lines were not altered (two lines of 500/500 debit/credit).
"""

from datetime import date


REF = "Bench Office Supplies Tmpl"


def check(env):
    failures = []

    moves = env["account.move"].search([
        ("move_type", "=", "entry"),
        ("ref", "=", REF),
    ])
    if len(moves) != 1:
        return [f"Expected exactly 1 journal entry with ref '{REF}', found {len(moves)}"]

    mv = moves[0]

    if mv.state != "draft":
        failures.append(f"Entry state is '{mv.state}', expected 'draft'")

    if mv.auto_post != "monthly":
        failures.append(
            f"auto_post is '{mv.auto_post}', expected 'monthly'"
        )

    expected_until = date(2026, 8, 1)
    if mv.auto_post_until != expected_until:
        failures.append(
            f"auto_post_until is '{mv.auto_post_until}', expected '{expected_until}'"
        )

    expected_date = date(2026, 5, 1)
    if mv.date != expected_date:
        failures.append(
            f"Accounting date is '{mv.date}', expected '{expected_date}' (must not be edited)"
        )

    lines = mv.line_ids.filtered(
        lambda l: l.display_type not in ("line_section", "line_note", "line_subsection")
    )
    if len(lines) != 2:
        failures.append(f"Expected exactly 2 journal lines, found {len(lines)}")

    total_debit = sum(line.debit for line in lines)
    total_credit = sum(line.credit for line in lines)
    if abs(total_debit - 500.0) > 0.01:
        failures.append(f"Total debit is {total_debit}, expected 500.00")
    if abs(total_credit - 500.0) > 0.01:
        failures.append(f"Total credit is {total_credit}, expected 500.00")

    return failures
