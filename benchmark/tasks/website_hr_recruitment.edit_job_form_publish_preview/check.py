"""Postcondition checks for website_hr_recruitment.edit_job_form_publish_preview.

Validates:
1. Exactly one hr.job "Bench QA Engineer" exists.
2. is_published is True (publish toggle was flipped).
3. description contains the exact phrase "Write automated tests for Bench Products.".
4. website_description still contains the seeded "Requirements" section with
   "Python, Playwright, 2+ yrs".
5. No new applicants were created.
"""

from odoo.tools import html2plaintext


JOB_NAME = "Bench QA Engineer"
EXPECTED_DESC_PHRASE = "Write automated tests for Bench Products."
REQUIRED_WEBSITE_DESC_TOKENS = ["Requirements", "Python", "Playwright", "2+ yrs"]


def check(env):
    failures = []

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
        failures.append(
            f"Job '{JOB_NAME}' is not published (is_published is False; "
            "expected True after toggling the Published switch)"
        )
    if not job.website_published:
        failures.append(
            f"Job '{JOB_NAME}' website_published is False; the Published "
            "boolean_toggle on the form should have set it True via its onchange"
        )

    # description content (HTML → plaintext, tolerant of surrounding markup)
    desc_text = html2plaintext(job.description or "")
    if EXPECTED_DESC_PHRASE not in desc_text:
        failures.append(
            f"Job description does not contain the exact phrase "
            f"{EXPECTED_DESC_PHRASE!r} (got: {desc_text!r})"
        )

    # website_description must still carry the seeded Requirements section.
    wdesc_text = html2plaintext(job.website_description or "")
    for token in REQUIRED_WEBSITE_DESC_TOKENS:
        if token not in wdesc_text:
            failures.append(
                f"Website description missing expected token {token!r} "
                "(seeded Requirements section was modified or removed)"
            )

    # No stray applicants.
    apps = env["hr.applicant"].with_context(active_test=False).search([
        ("job_id", "=", job.id),
    ])
    if apps:
        failures.append(
            f"Unexpected applicants created/linked to '{JOB_NAME}': "
            f"{apps.mapped('partner_name')!r}"
        )

    # Department / recruitment count must not have been tampered with.
    if job.department_id.name != "Administration":
        failures.append(
            f"Job department changed to {job.department_id.name!r}; "
            "expected 'Administration' (seeded)"
        )
    if job.no_of_recruitment != 1:
        failures.append(
            f"Job no_of_recruitment is {job.no_of_recruitment}; "
            "expected 1 (seeded)"
        )

    return failures
