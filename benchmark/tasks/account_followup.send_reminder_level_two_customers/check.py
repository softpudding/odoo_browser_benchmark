"""Postcondition checks for account_followup.send_reminder_level_two_customers.

BLOCKED TASK — `account_followup` addon is not vendored in this
Odoo 19 Community checkout, so the task cannot run end-to-end. The
check below returns a clear failure string so the eval pipeline flags
it rather than appearing as a spurious PASS.
"""


def check(env):
    module = env["ir.module.module"].search(
        [("name", "=", "account_followup")], limit=1
    )
    if not module or module.state != "installed":
        return [
            "BLOCKED: `account_followup` addon is not available in this "
            "Odoo Community checkout (Enterprise-only). Task cannot be "
            "validated end-to-end. See STATUS.md row 404 for re-enabling "
            "notes."
        ]

    # Concrete validation to add once the addon is vendored:
    #   - exactly one `res.partner` named 'Bench Overdue Co'.
    #   - exactly 3 posted `account.move` rows with names
    #     OV/BENCH/001..003 for this partner, all state='posted',
    #     payment_state='not_paid', invoice_date_due = today - 45d.
    #   - at least one `mail.message` logged on the partner whose body
    #     contains all three invoice names.
    #   - partner's `followup_status` advanced from
    #     'in_need_of_action' / level-2 chip cleared.
    #   - at least one `mail.mail` (or outgoing mail.message) exists
    #     whose recipient_ids includes the partner or email_to matches
    #     the partner's email.
    return [
        "BLOCKED: account_followup addon became available but check body "
        "not yet implemented. See STATUS.md row 404 for context."
    ]
