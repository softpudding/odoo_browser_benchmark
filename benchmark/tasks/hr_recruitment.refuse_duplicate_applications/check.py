"""Postcondition checks for hr_recruitment.refuse_duplicate_applications."""


TARGET_EMAIL = "priya.nair@example.com"
DISTRACTOR_NAME = "Priya Narayan"
EXPECTED_REASON = "Candidate withdrew"
EXPECTED_SUBJECT = "Operations Analyst application update"
EXPECTED_BODY = (
    "We are closing your Operations Analyst applications after your withdrawal request."
)
PRIMARY_APPLICANT = "Priya Nair"


def check(env):
    failures = []

    applicants = env["hr.applicant"].with_context(active_test=False).search(
        [("email_from", "=", TARGET_EMAIL)]
    )
    distractor = env["hr.applicant"].with_context(active_test=False).search(
        [("partner_name", "=", DISTRACTOR_NAME)], limit=1
    )

    if len(applicants) != 2:
        return [f"Expected 2 refused target applicants, found {len(applicants)}"]
    if not distractor:
        return [f"Distractor applicant {DISTRACTOR_NAME!r} not found"]

    for applicant in applicants:
        if applicant.active:
            failures.append(f"{applicant.partner_name} is still active")
        if applicant.refuse_reason_id.name != EXPECTED_REASON:
            failures.append(
                f"{applicant.partner_name} refusal reason is {applicant.refuse_reason_id.name!r}, expected {EXPECTED_REASON!r}"
            )
        if applicant.partner_name == PRIMARY_APPLICANT:
            messages = env["mail.message"].search(
                [
                    ("model", "=", "hr.applicant"),
                    ("res_id", "=", applicant.id),
                    ("subject", "=", EXPECTED_SUBJECT),
                ],
                order="id desc",
            )
            if not messages:
                failures.append(f"{applicant.partner_name} is missing the expected refusal email")
            elif EXPECTED_BODY.lower() not in (messages[0].body or "").lower():
                failures.append(f"{applicant.partner_name} refusal email body is incorrect")

    if not distractor.active:
        failures.append("Distractor applicant was refused")
    if distractor.refuse_reason_id:
        failures.append("Distractor applicant received a refusal reason")

    return failures
