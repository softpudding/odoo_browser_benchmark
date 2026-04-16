"""Clean up artifacts from previous runs."""


JOB_NAME = "Senior Platform Engineer"


def cleanup(env):
    apps = env["hr.applicant"].with_context(active_test=False).search(
        [("job_id.name", "=", JOB_NAME)]
    )
    for app in apps:
        env["mail.message"].search([
            ("res_model", "=", "hr.applicant"),
            ("res_id", "=", app.id),
        ]).unlink()
        app.unlink()
