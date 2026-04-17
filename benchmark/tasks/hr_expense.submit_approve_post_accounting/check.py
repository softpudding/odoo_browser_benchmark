"""Postcondition checks for hr_expense.submit_approve_post_accounting."""


REPORT_NAME = "TRV-2026-04 – April client visit"


def check(env):
    failures = []

    sheets = env["hr.expense.sheet"].search([("name", "=", REPORT_NAME)])
    if not sheets:
        return [f"No expense report found named '{REPORT_NAME}'"]
    if len(sheets) > 1:
        failures.append(f"Found {len(sheets)} reports, expected 1")
    sheet = sheets[0]

    # Accept either 'post' or 'done' depending on Odoo version.
    if sheet.state not in ("post", "done"):
        failures.append(
            f"Report state is '{sheet.state}', expected 'post' or 'done' "
            f"(fully posted to accounting)"
        )

    # Verify a journal entry (account.move) is linked.
    moves = getattr(sheet, "account_move_ids", None)
    if moves is None:
        # Single-move field on some versions.
        move = getattr(sheet, "account_move_id", None)
        moves = move if move else env["account.move"]
    if not moves:
        failures.append(
            "No journal entry (account.move) is linked to the report — "
            "the report must be posted to accounting"
        )
    else:
        any_posted = any(m.state == "posted" for m in moves)
        if not any_posted:
            failures.append(
                "Linked journal entry exists but is not posted — expected at "
                "least one posted account.move"
            )

    return failures
