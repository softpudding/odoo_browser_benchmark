"""Postcondition checks for hr_recruitment.refuse_applicant_with_reason.

Validates:
1. Target applicant 'Marcus Whitfield' on job 'Senior Platform Engineer'
   is refused (active=False) with the expected refuse reason.
2. The two distractor applicants on the same job remain active and have
   no refuse reason set.
"""


JOB_NAME = "Senior Platform Engineer"
TARGET = "Marcus Whitfield"
DISTRACTORS = ["Ella Navarro", "Devon Burke"]
EXPECTED_REASON = "Does not fit the job requirements"


def check(env):
    failures = []

    Applicant = env["hr.applicant"].with_context(active_test=False)

    target = Applicant.search([
        ("partner_name", "=", TARGET),
        ("job_id.name", "=", JOB_NAME),
    ], limit=1)
    if not target:
        return [f"Target applicant '{TARGET}' on job '{JOB_NAME}' not found"]

    if target.active:
        failures.append(
            f"Target applicant '{TARGET}' is still active (expected refused)"
        )
    if not target.refuse_reason_id:
        failures.append(
            f"Target applicant '{TARGET}' has no refuse_reason_id set"
        )
    elif target.refuse_reason_id.name != EXPECTED_REASON:
        failures.append(
            f"Refuse reason is '{target.refuse_reason_id.name}', "
            f"expected '{EXPECTED_REASON}'"
        )

    for name in DISTRACTORS:
        other = Applicant.search([
            ("partner_name", "=", name),
            ("job_id.name", "=", JOB_NAME),
        ], limit=1)
        if not other:
            failures.append(f"Distractor applicant '{name}' is missing")
            continue
        if not other.active:
            failures.append(
                f"Distractor applicant '{name}' was archived (expected active)"
            )
        if other.refuse_reason_id:
            failures.append(
                f"Distractor applicant '{name}' has refuse_reason_id "
                f"'{other.refuse_reason_id.name}' (expected none)"
            )

    return failures
