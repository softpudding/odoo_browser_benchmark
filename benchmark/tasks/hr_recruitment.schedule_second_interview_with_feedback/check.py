"""Postcondition checks for hr_recruitment.schedule_second_interview_with_feedback."""


TARGET_NAME = "Mina Chen"
DISTRACTOR_NAME = "Mina Chen West"
FEEDBACK = "Strong process knowledge and clear stakeholder communication."


def check(env):
    failures = []

    applicant = env["hr.applicant"].search([("partner_name", "=", TARGET_NAME)], limit=1)
    if not applicant:
        return [f"Applicant '{TARGET_NAME}' not found"]

    if applicant.stage_id.name != "Second Interview":
        failures.append(
            f"Applicant stage is '{applicant.stage_id.name}', expected 'Second Interview'"
        )
    if FEEDBACK not in (applicant.applicant_notes or ""):
        failures.append("Applicant notes do not contain the required feedback text")

    meetings = env["calendar.event"].search([
        ("applicant_id", "=", applicant.id),
        ("name", "=", "Second Interview - Mina Chen"),
    ])
    if len(meetings) != 1:
        failures.append(f"Expected exactly 1 second interview meeting, found {len(meetings)}")
    else:
        meeting = meetings[0]
        if str(meeting.start) != "2026-06-25 14:00:00":
            failures.append(f"Meeting start is {meeting.start}, expected 2026-06-25 14:00:00")
        if str(meeting.stop) != "2026-06-25 14:30:00":
            failures.append(f"Meeting end is {meeting.stop}, expected 2026-06-25 14:30:00")

    distractor = env["hr.applicant"].search([("partner_name", "=", DISTRACTOR_NAME)], limit=1)
    if not distractor:
        failures.append(f"Distractor applicant '{DISTRACTOR_NAME}' not found")
    else:
        if distractor.stage_id.name != "First Interview":
            failures.append("Distractor applicant stage should remain 'First Interview'")
        if distractor.applicant_notes:
            failures.append("Distractor applicant should not receive interview feedback")

    return failures
