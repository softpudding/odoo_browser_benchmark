"""Postcondition checks for website_hr_recruitment.apply_guru_job.

Validates conditions that cannot be expressed as state-spec field diffs,
such as chatter message content containing the required introduction text.
"""

from odoo.tools import html2plaintext


def check(env):
    """Return a list of failure messages (empty list = all checks pass)."""
    failures = []

    # Find the applicant created by this task
    applicant = env["hr.applicant"].search([
        ("partner_name", "=", "John Smith"),
        ("email_from", "=", "john@smith.com"),
    ], limit=1)

    if not applicant:
        failures.append("No hr.applicant found for John Smith / john@smith.com")
        return failures

    # Check that the short introduction appears in the chatter
    intro_text = "### [GURU] HR RECRUITMENT TEST DATA ###"
    messages = applicant.message_ids.mapped(lambda m: html2plaintext(m.body))
    if not any(intro_text in msg for msg in messages):
        failures.append(
            f"Required short introduction '{intro_text}' not found in "
            f"applicant chatter messages"
        )

    return failures
