"""Cleanup for hr_expense.split_submitted_report_resubmit.

Reverses the seed: removes the three R-BENCH-SPLIT-001 expenses plus any
split children so a fresh run starts clean.
"""

EXPENSE_NAMES = [
    "R-BENCH-SPLIT-001 Meal",
    "R-BENCH-SPLIT-001 Gadget",
    "R-BENCH-SPLIT-001 Taxi",
]


def cleanup(env):
    expenses = env["hr.expense"].with_context(active_test=False).search([
        ("name", "in", EXPENSE_NAMES),
    ])
    for exp in expenses:
        children = env["hr.expense"].with_context(active_test=False).search([
            ("split_expense_origin_id", "=", exp.id),
        ])
        for child in children:
            try:
                if child.state != "draft":
                    child.action_reset()
            except Exception:
                pass
            try:
                if child.account_move_id:
                    if child.account_move_id.state == "posted":
                        child.account_move_id.button_draft()
                    child.account_move_id.unlink()
            except Exception:
                pass
            child.unlink()
        try:
            if exp.state != "draft":
                exp.action_reset()
        except Exception:
            pass
        try:
            if exp.account_move_id:
                if exp.account_move_id.state == "posted":
                    exp.account_move_id.button_draft()
                exp.account_move_id.unlink()
        except Exception:
            pass
        attachments = env["ir.attachment"].search([
            ("res_model", "=", "hr.expense"),
            ("res_id", "=", exp.id),
        ])
        attachments.unlink()
        exp.unlink()
