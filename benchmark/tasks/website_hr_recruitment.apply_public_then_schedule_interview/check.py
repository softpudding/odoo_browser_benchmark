"""Postcondition checks for website_hr_recruitment.apply_public_then_schedule_interview."""

from datetime import date
from odoo.tools import html2plaintext


JOB_NAME = "Platform Support Analyst"
APPLICANT_NAME = "Casey Portal"
APPLICANT_EMAIL = "casey.portal@example.com"
INTRO_TEXT = "Public applicant ready for interview scheduling."


def check(env):
    failures = []

    applicant = env["hr.applicant"].search([
        ("partner_name", "=", APPLICANT_NAME),
        ("email_from", "=", APPLICANT_EMAIL),
    ], limit=1)
    if not applicant:
        return [f"No hr.applicant found for {APPLICANT_NAME} / {APPLICANT_EMAIL}"]

    if applicant.job_id.name != JOB_NAME:
        failures.append(
            f"Applicant job is {applicant.job_id.name!r}, expected {JOB_NAME!r}"
        )

    messages = applicant.message_ids.mapped(lambda m: html2plaintext(m.body))
    if not any(INTRO_TEXT in msg for msg in messages):
        failures.append(
            f"Required short introduction {INTRO_TEXT!r} not found in applicant chatter"
        )

    marc = env["res.users"].search([("login", "=", "marc.demo")], limit=1)
    if not marc:
        failures.append("Marc Demo user not found")
        return failures

    activities = env["mail.activity"].search([
        ("res_model", "=", "hr.applicant"),
        ("res_id", "=", applicant.id),
    ])
    if not activities:
        failures.append("No activity found on Casey Portal applicant")
        return failures

    call_type = env["mail.activity.type"].search([("name", "ilike", "Call")], limit=1)
    act = activities.filtered(lambda a: a.activity_type_id.id == call_type.id)[:1] if call_type else activities[:1]
    if not act:
        failures.append("No Call activity found on Casey Portal applicant")
        return failures
    act = act[0]
    if act.user_id.id != marc.id:
        failures.append(
            f"Activity assigned to {act.user_id.name!r}, expected 'Marc Demo'"
        )
    if act.date_deadline != date(2026, 5, 28):
        failures.append(
            f"Activity due date is {act.date_deadline}, expected 2026-05-28"
        )
    if (act.summary or "") != "Schedule initial interview":
        failures.append(
            f"Activity summary is {act.summary!r}, expected 'Schedule initial interview'"
        )

    return failures
