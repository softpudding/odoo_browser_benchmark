"""Cleanup for hr_recruitment.schedule_interview_for_applicant."""


def cleanup(env):
    applicants = env["hr.applicant"].search([
        ("partner_name", "in", ["Riley Mercer", "Riley Mercer West"]),
    ])
    if applicants:
        env["mail.activity"].search([
            ("res_model", "=", "hr.applicant"),
            ("res_id", "in", applicants.ids),
        ]).unlink()
        applicants.unlink()
    env["mail.activity"].search([("summary", "=", "Schedule first interview")]).unlink()
