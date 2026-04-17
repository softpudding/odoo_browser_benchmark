"""Cleanup for hr_recruitment.schedule_second_interview_with_feedback."""


def cleanup(env):
    applicants = env["hr.applicant"].search([
        ("partner_name", "in", ["Mina Chen", "Mina Chen West"]),
    ])
    if applicants:
        env["calendar.event"].search([("applicant_id", "in", applicants.ids)]).unlink()
        applicants.unlink()
