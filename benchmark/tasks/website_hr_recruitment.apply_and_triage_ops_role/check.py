"""Postcondition checks for website_hr_recruitment.apply_and_triage_ops_role."""

from odoo.tools import html2plaintext


def check(env):
    failures = []

    applicant = env["hr.applicant"].search([
        ("partner_name", "=", "Jack Doe"),
        ("email_from", "=", "jack@doe.com"),
    ], limit=1)
    if not applicant:
        return ["No hr.applicant found for Jack Doe / jack@doe.com"]

    if applicant.stage_id.name != "Qualification":
        failures.append(
            f"Applicant stage is {applicant.stage_id.name!r}, expected 'Qualification'"
        )

    if applicant.priority != "3":
        failures.append(f"Applicant priority is {applicant.priority!r}, expected '3'")

    intro_text = "### [CS-SPECIALIST] HR TEST ###"
    messages = applicant.message_ids.mapped(lambda m: html2plaintext(m.body))
    if not any(intro_text in msg for msg in messages):
        failures.append(
            f"Required short introduction '{intro_text}' not found in applicant chatter"
        )

    referral_text = "Referral Code : CUST-REF-27"
    if not any(referral_text in msg for msg in messages):
        failures.append(
            f"Required custom field payload '{referral_text}' not found in applicant chatter"
        )

    notes_text = "Implementation Notes : Escalate onboarding blockers"
    if not any(notes_text in msg for msg in messages):
        failures.append(
            f"Required custom field payload '{notes_text}' not found in applicant chatter"
        )

    if applicant.job_id.name != "Customer Success Specialist":
        failures.append(
            f"Applicant job is {applicant.job_id.name!r}, expected 'Customer Success Specialist'"
        )

    return failures
