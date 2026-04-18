"""Postcondition checks for website_hr_recruitment.publish_job_from_backoffice_then_apply_portal."""

from odoo.tools import html2plaintext


JOB_NAME = "Senior Widget Engineer"
APPLICANT_NAME = "Alex Portal"
APPLICANT_EMAIL = "alex.portal@example.com"


def check(env):
    failures = []

    # ---- Job side ----
    jobs = env["hr.job"].with_context(active_test=False).search([
        ("name", "=", JOB_NAME),
    ])
    if not jobs:
        return [f"No hr.job found with name '{JOB_NAME}'"]
    if len(jobs) > 1:
        failures.append(
            f"Expected exactly 1 hr.job named '{JOB_NAME}', found {len(jobs)}"
        )
    job = jobs[0]

    if not job.is_published:
        failures.append(f"Job '{JOB_NAME}' is not published (is_published is False)")

    # website_id may be null even when is_published=True in a single-website
    # instance; we only require is_published=True.

    if job.department_id.name != "Administration":
        failures.append(
            f"Job '{JOB_NAME}' department is "
            f"{job.department_id.name!r}, expected 'Administration'"
        )

    if job.no_of_recruitment != 2:
        failures.append(
            f"Job '{JOB_NAME}' no_of_recruitment is "
            f"{job.no_of_recruitment}, expected 2"
        )

    desc_text = html2plaintext(job.description or "")
    if "Design and build widgets" not in desc_text:
        failures.append(
            f"Job '{JOB_NAME}' description does not contain "
            f"'Design and build widgets' (got: {desc_text!r})"
        )

    # ---- Applicant side ----
    applicants = env["hr.applicant"].with_context(active_test=False).search([
        "|",
        ("partner_name", "=", APPLICANT_NAME),
        ("email_from", "=", APPLICANT_EMAIL),
    ])
    if not applicants:
        failures.append(
            f"No hr.applicant found for '{APPLICANT_NAME}' / "
            f"'{APPLICANT_EMAIL}'"
        )
        return failures

    # Find the one for our job (other distractors should not exist)
    applicant = applicants.filtered(lambda a: a.job_id == job)
    if not applicant:
        failures.append(
            f"Applicant '{APPLICANT_NAME}' is not linked to job '{JOB_NAME}' "
            f"(linked job(s): {applicants.mapped('job_id.name')!r})"
        )
        return failures
    if len(applicant) > 1:
        failures.append(
            f"Expected exactly 1 applicant for '{APPLICANT_NAME}' on job "
            f"'{JOB_NAME}', found {len(applicant)}"
        )
    a = applicant[0]

    if APPLICANT_EMAIL.lower() not in (a.email_from or "").lower():
        failures.append(
            f"Applicant email_from is {a.email_from!r}, expected to contain "
            f"{APPLICANT_EMAIL!r}"
        )

    intro_text = "Excited to apply for this role"
    messages = a.message_ids.mapped(lambda m: html2plaintext(m.body))
    if not any(intro_text in msg for msg in messages):
        failures.append(
            f"Required short introduction containing {intro_text!r} not "
            f"found in applicant chatter messages"
        )

    # ---- No extra jobs / no extra applicants ----
    extra_jobs = env["hr.job"].search([
        ("name", "=", JOB_NAME),
    ])
    if len(extra_jobs) != 1:
        failures.append(
            f"Expected exactly 1 active job named '{JOB_NAME}', found {len(extra_jobs)}"
        )

    return failures
