"""Clean up artifacts from previous runs of
hr_recruitment.create_applicant_kanban_move_to_offer."""


JOB_NAME = "Bench Senior Dev"
DEPARTMENT_NAME = "Bench Engineering"
APPLICANT_NAME = "Alice Applicant"
STAGE_NAMES = [
    "Initial Qualification",
    "Qualified",
    "Contract Proposal",
    "Contract Signed",
]


def cleanup(env):
    # Applicants first (they reference stage_id, job_id)
    apps = env["hr.applicant"].with_context(active_test=False).search([
        "|",
        ("partner_name", "=", APPLICANT_NAME),
        ("email_from", "=", "alice@bench.test"),
    ])
    for a in apps:
        env["mail.message"].sudo().search([
            ("model", "=", "hr.applicant"),
            ("res_id", "=", a.id),
        ]).unlink()
    apps.unlink()

    # Job + stages
    job = env["hr.job"].with_context(active_test=False).search(
        [("name", "=", JOB_NAME)], limit=1
    )
    if job:
        # Any leftover applicants still linked (safety)
        env["hr.applicant"].with_context(active_test=False).search([
            ("job_id", "=", job.id),
        ]).unlink()
        # Detach our canonical stages; if they orphan out, drop them.
        stages = env["hr.recruitment.stage"].with_context(
            active_test=False
        ).search([("job_ids", "in", [job.id])])
        for stage in stages:
            stage.write({"job_ids": [(3, job.id)]})
            if not stage.job_ids and stage.name in STAGE_NAMES:
                refs = env["hr.applicant"].with_context(
                    active_test=False
                ).search_count([("stage_id", "=", stage.id)])
                if refs == 0:
                    stage.unlink()
        job.unlink()

    # Last-resort: orphan canonical stages (no job) with no applicants
    for sname in STAGE_NAMES:
        orphans = env["hr.recruitment.stage"].with_context(
            active_test=False
        ).search([("name", "=", sname)])
        for s in orphans:
            if not s.job_ids:
                refs = env["hr.applicant"].with_context(
                    active_test=False
                ).search_count([("stage_id", "=", s.id)])
                if refs == 0:
                    s.unlink()

    # Department — only drop if empty (not used by other jobs/employees)
    dept = env["hr.department"].search(
        [("name", "=", DEPARTMENT_NAME)], limit=1
    )
    if dept:
        in_use = (
            env["hr.job"].search_count([("department_id", "=", dept.id)]) +
            env["hr.employee"].with_context(active_test=False).search_count([
                ("department_id", "=", dept.id)
            ])
        )
        if in_use == 0:
            dept.unlink()
