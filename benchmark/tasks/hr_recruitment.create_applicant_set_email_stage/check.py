"""Postcondition checks for hr_recruitment.create_applicant_set_email_stage.

Validates:
1. Applicant "Taylor Kim" exists
2. Stage is "First Interview"
3. Appreciation/priority is "1" (In Progress / medium)
4. Description/application summary contains expected text
"""

APPLICANT_NAME = "Taylor Kim"


def check(env):
    failures = []

    app = env["hr.applicant"].search([
        ("partner_name", "=", APPLICANT_NAME),
    ], limit=1)

    if not app:
        return [f"Applicant '{APPLICANT_NAME}' not found"]

    # Check stage
    if not app.stage_id or app.stage_id.name != "First Interview":
        failures.append(
            f"Stage is '{app.stage_id.name if app.stage_id else 'None'}', "
            "expected 'First Interview'"
        )

    # Check appreciation / priority
    if app.priority != "1":
        failures.append(
            f"Appreciation/priority is '{app.priority}', expected '1' (In Progress)"
        )

    # Check applicant notes / summary
    notes = app.applicant_notes or ""
    import re
    notes_text = re.sub(r"<[^>]+>", "", notes).strip().lower()
    if "technical" not in notes_text or "interview" not in notes_text:
        failures.append(
            "Applicant notes do not contain expected text about "
            "technical background and interview"
        )

    # Check unchanged fields
    if app.email_from and "taylor.kim" not in app.email_from:
        failures.append(
            f"Email changed to '{app.email_from}', expected to contain 'taylor.kim'"
        )

    return failures
