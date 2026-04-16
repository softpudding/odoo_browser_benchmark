"""Postcondition checks for hr_recruitment.schedule_interview_for_applicant."""

from datetime import date


def check(env):
    failures = []

    applicant = env["hr.applicant"].search([
        ("partner_name", "=", "Riley Mercer"),
    ], limit=1)
    if not applicant:
        return ["Applicant 'Riley Mercer' not found"]

    if applicant.stage_id.name != "Initial Qualification":
        failures.append(
            f"Applicant stage is '{applicant.stage_id.name}', expected 'Initial Qualification'"
        )

    activities = env["mail.activity"].search([
        ("res_model", "=", "hr.applicant"),
        ("res_id", "=", applicant.id),
        ("summary", "=", "Schedule first interview"),
    ])
    if len(activities) != 1:
        failures.append(
            f"Expected exactly 1 matching activity on the applicant, found {len(activities)}"
        )
    else:
        activity = activities[0]
        if activity.activity_type_id.name != "Call":
            failures.append(
                f"Activity type is '{activity.activity_type_id.name}', expected 'Call'"
            )
        if activity.date_deadline != date(2026, 6, 17):
            failures.append(
                f"Activity due date is {activity.date_deadline}, expected 2026-06-17"
            )

    distractor = env["hr.applicant"].search([
        ("partner_name", "=", "Riley Mercer West"),
    ], limit=1)
    if not distractor:
        failures.append("Distractor applicant 'Riley Mercer West' not found")
    else:
        distractor_activities = env["mail.activity"].search([
            ("res_model", "=", "hr.applicant"),
            ("res_id", "=", distractor.id),
        ])
        if distractor_activities:
            failures.append("Distractor applicant should not have any scheduled activities")

    return failures
