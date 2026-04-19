"""Clean up artifacts from prior runs of
hr_recruitment.hire_candidate_refuse_another."""

JOB_NAME = "Bench Role"
DEPARTMENT_NAME = "Bench Department"
TOP_NAME = "Top Candidate"
RUNNER_NAME = "Runner Up"
TOP_EMAIL = "top.candidate@bench.test"
RUNNER_EMAIL = "runner.up@bench.test"
REFUSE_REASON = "Not a fit"
DISTRACTOR_REASONS = [
    "Not a good fit",
    "Not a fit - incomplete application",
]
STAGE_NAMES = [
    "Initial Qualification",
    "Qualified",
    "Contract Proposal",
    "Contract Signed",
]


def cleanup(env):
    # 1. Employees created by the applicant hire (must go before
    #    applicants if hr.employee.applicant_ids is the link, but
    #    hr.applicant.employee_id restricts — clear the link first).
    Applicant = env["hr.applicant"].with_context(active_test=False)
    apps = Applicant.search([
        "|",
        ("partner_name", "in", [TOP_NAME, RUNNER_NAME]),
        ("email_from", "in", [TOP_EMAIL, RUNNER_EMAIL]),
    ])
    for app in apps:
        if app.employee_id:
            emp = app.employee_id
            app.employee_id = False
            emp.unlink()
        env["mail.message"].sudo().search([
            ("model", "=", "hr.applicant"),
            ("res_id", "=", app.id),
        ]).unlink()
    apps.unlink()

    # Orphan employees matching our names (no active applicant link)
    env["hr.employee"].with_context(active_test=False).search(
        [("name", "in", [TOP_NAME, RUNNER_NAME])]
    ).unlink()

    # 2. Job + its scoped stages
    job = env["hr.job"].with_context(active_test=False).search(
        [("name", "=", JOB_NAME)], limit=1
    )
    if job:
        env["hr.applicant"].with_context(active_test=False).search(
            [("job_id", "=", job.id)]
        ).unlink()
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

    # 3. Refuse reasons (primary + distractors)
    all_reason_names = [REFUSE_REASON] + DISTRACTOR_REASONS
    reasons = env["hr.applicant.refuse.reason"].with_context(
        active_test=False
    ).search([("name", "in", all_reason_names)])
    env["hr.applicant"].with_context(active_test=False).search([
        ("refuse_reason_id", "in", reasons.ids)
    ]).write({"refuse_reason_id": False})
    reasons.unlink()

    # 4. Department — only drop if unused
    dept = env["hr.department"].search(
        [("name", "=", DEPARTMENT_NAME)], limit=1
    )
    if dept:
        in_use = (
            env["hr.job"].search_count([("department_id", "=", dept.id)])
            + env["hr.employee"].with_context(active_test=False).search_count(
                [("department_id", "=", dept.id)]
            )
        )
        if in_use == 0:
            dept.unlink()
