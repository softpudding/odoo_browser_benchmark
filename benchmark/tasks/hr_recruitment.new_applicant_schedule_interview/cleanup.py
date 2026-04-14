"""Clean up artifacts from previous runs."""


def cleanup(env):
    # Remove Elena Vasquez applicant and her activities
    applicants = env["hr.applicant"].search([
        ("partner_name", "=", "Elena Vasquez"),
    ])
    if applicants:
        env["mail.activity"].search([
            ("res_model", "=", "hr.applicant"),
            ("res_id", "in", applicants.ids),
        ]).unlink()
        applicants.unlink()

    # Remove distractor
    distractors = env["hr.applicant"].search([
        ("partner_name", "=", "Alex Kemp"),
    ])
    if distractors:
        env["mail.activity"].search([
            ("res_model", "=", "hr.applicant"),
            ("res_id", "in", distractors.ids),
        ]).unlink()
        distractors.unlink()

    # Remove job position (only our seeded one)
    job = env["hr.job"].search([("name", "=", "Senior Backend Developer")])
    if job:
        remaining = env["hr.applicant"].search([("job_id", "in", job.ids)])
        if remaining:
            env["mail.activity"].search([
                ("res_model", "=", "hr.applicant"),
                ("res_id", "in", remaining.ids),
            ]).unlink()
            remaining.unlink()
        job.unlink()

    # Remove Marc Demo user only if we created it (check for seed marker)
    marc = env["res.users"].search([("login", "=", "marc.demo")])
    if marc:
        # Only remove if the user has no records beyond what our seed created
        other_applicants = env["hr.applicant"].search([
            ("user_id", "=", marc.id),
            ("partner_name", "not in", ["Elena Vasquez", "Alex Kemp"]),
        ])
        if not other_applicants:
            marc.write({"active": False})
            marc.unlink()

    # Remove Development department if empty
    dept = env["hr.department"].search([("name", "=", "Development")])
    if dept:
        other_jobs = env["hr.job"].search([("department_id", "=", dept.id)])
        if not other_jobs:
            dept.unlink()
