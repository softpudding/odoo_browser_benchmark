"""Seed for hr_recruitment.hire_candidate_refuse_another.

Category: policy_trap_wizard (HARD).

Two applicants on a single seeded job. The agent has to:
 (a) Advance 'Top Candidate' to the hired stage (Contract Signed,
     which has hired_stage=True, thereby setting date_closed) AND
     click the 'Create Employee' header button that appears once the
     stage is hired. That call is ``create_employee_from_applicant``
     which creates an ``hr.employee`` and links it back via
     ``hr.applicant.employee_id``. The wizard-style 2nd phase (the
     pre-filled employee form that must still be saved) is the main
     policy trap — BU often aborts after seeing the Hired ribbon and
     never creates / saves the employee record.
 (b) Refuse 'Runner Up' via the archive_applicant button, which opens
     the ``applicant.get.refuse.reason`` wizard. The agent must pick
     the seeded ``Not a fit`` refuse reason (one of several) and apply.

The seed ensures:
 - ``Contract Signed`` stage with hired_stage=True is available on the
   Bench Role job. The default demo data already ships a global
   ``Contract Signed`` stage, but we create a job-scoped copy so the
   Applications kanban renders exactly the four seeded columns even if
   the demo ones are missing.
 - A fresh refuse reason named ``Not a fit`` exists (distinct from
   the default demo reasons, which include ``Does not fit the job
   requirements``). The prompt names this reason precisely to force
   the agent to pick the right badge among many.
"""


JOB_NAME = "Bench Role"
DEPARTMENT_NAME = "Bench Department"

TOP_NAME = "Top Candidate"
RUNNER_NAME = "Runner Up"
TOP_EMAIL = "top.candidate@bench.test"
RUNNER_EMAIL = "runner.up@bench.test"

REFUSE_REASON = "Not a fit"

STAGE_SEQUENCE = [
    ("Initial Qualification", 10, False),
    ("Qualified", 20, False),
    ("Contract Proposal", 30, False),
    ("Contract Signed", 40, True),
]


def _ensure_department(env, name):
    dept = env["hr.department"].search([("name", "=", name)], limit=1)
    if not dept:
        dept = env["hr.department"].create({"name": name})
    return dept


def _cleanup_applicants_and_employee(env):
    Applicant = env["hr.applicant"].with_context(active_test=False)
    old = Applicant.search([
        "|",
        ("partner_name", "in", [TOP_NAME, RUNNER_NAME]),
        ("email_from", "in", [TOP_EMAIL, RUNNER_EMAIL]),
    ])
    # Delete any linked employee first (if a prior run created one)
    Employee = env["hr.employee"].with_context(active_test=False)
    for app in old:
        if app.employee_id:
            emp = app.employee_id
            # Detach first to avoid ondelete restrict cycles
            app.employee_id = False
            emp.unlink()
    # Also drop orphan employees by name (safety)
    orphans = Employee.search([("name", "in", [TOP_NAME, RUNNER_NAME])])
    orphans.unlink()
    # Drop any chatter
    for app in old:
        env["mail.message"].sudo().search([
            ("model", "=", "hr.applicant"),
            ("res_id", "=", app.id),
        ]).unlink()
    old.unlink()


def _cleanup_job_and_stages(env):
    job = env["hr.job"].with_context(active_test=False).search(
        [("name", "=", JOB_NAME)], limit=1
    )
    if job:
        # Unlink any employee still referencing this job from a prior run
        env["hr.employee"].with_context(active_test=False).search([
            ("job_id", "=", job.id),
            ("name", "in", [TOP_NAME, RUNNER_NAME]),
        ]).unlink()
        # Any applicants still on the job
        env["hr.applicant"].with_context(active_test=False).search([
            ("job_id", "=", job.id),
        ]).unlink()
        our_names = [n for n, _, _ in STAGE_SEQUENCE]
        stages = env["hr.recruitment.stage"].with_context(
            active_test=False
        ).search([("job_ids", "in", [job.id])])
        for stage in stages:
            stage.write({"job_ids": [(3, job.id)]})
            if not stage.job_ids and stage.name in our_names:
                refs = env["hr.applicant"].with_context(
                    active_test=False
                ).search_count([("stage_id", "=", stage.id)])
                if refs == 0:
                    stage.unlink()
        job.unlink()


DISTRACTOR_REASONS = [
    "Not a good fit",
    "Not a fit - incomplete application",
]


def _cleanup_refuse_reason(env):
    names = [REFUSE_REASON] + DISTRACTOR_REASONS
    old = env["hr.applicant.refuse.reason"].with_context(
        active_test=False
    ).search([("name", "in", names)])
    # Detach from any lingering applicants first
    env["hr.applicant"].with_context(active_test=False).search([
        ("refuse_reason_id", "in", old.ids),
    ]).write({"refuse_reason_id": False})
    old.unlink()


def setup(env):
    # 1. Cleanup in child-first order
    _cleanup_applicants_and_employee(env)
    _cleanup_job_and_stages(env)
    _cleanup_refuse_reason(env)

    # 2. Department + job
    dept = _ensure_department(env, DEPARTMENT_NAME)
    job = env["hr.job"].create({
        "name": JOB_NAME,
        "department_id": dept.id,
        "no_of_recruitment": 1,
    })

    # 3. Four stages scoped to this job (so the kanban shows exactly
    #    these columns + any global stages). The last stage has
    #    hired_stage=True so clicking it triggers date_closed.
    stages_by_name = {}
    for sname, seq, hired in STAGE_SEQUENCE:
        stages_by_name[sname] = env["hr.recruitment.stage"].create({
            "name": sname,
            "sequence": seq,
            "hired_stage": hired,
            "fold": hired,  # Contract Signed is folded in demo too
            "job_ids": [(6, 0, [job.id])],
        })
    init_stage = stages_by_name["Initial Qualification"]

    # 4. Refuse reasons: the task-specific one PLUS two near-duplicates
    #    to create a selection trap. Agents tend to read "Not a fit"
    #    and then pick the first badge that contains those words —
    #    "Not a good fit" + "Not a fit - incomplete application"
    #    are visually plausible substitutes.
    #
    #    All reasons get no template so the wizard's send_mail toggle
    #    defaults to False (the agent doesn't need to toggle it off).
    #    The stock demo reasons (Does not fit..., Duplicate, Spam,
    #    ...) remain visible as badges, so the agent has to pick the
    #    right one among many.
    for sname, seq in [
        (REFUSE_REASON, 5),
        ("Not a good fit", 6),
        ("Not a fit - incomplete application", 7),
    ]:
        env["hr.applicant.refuse.reason"].create({
            "name": sname,
            "sequence": seq,
        })

    # 5. Two applicants — both active, both in Initial Qualification
    env["hr.applicant"].create({
        "partner_name": TOP_NAME,
        "email_from": TOP_EMAIL,
        "partner_phone": "+1 555 0111",
        "job_id": job.id,
        "stage_id": init_stage.id,
        "department_id": dept.id,
        "active": True,
    })
    env["hr.applicant"].create({
        "partner_name": RUNNER_NAME,
        "email_from": RUNNER_EMAIL,
        "partner_phone": "+1 555 0222",
        "job_id": job.id,
        "stage_id": init_stage.id,
        "department_id": dept.id,
        "active": True,
    })

    # Sanity checks
    assert env["hr.applicant"].search_count([
        ("job_id", "=", job.id),
        ("active", "=", True),
    ]) == 2, "Expected exactly 2 active applicants on Bench Role"
    assert env["hr.applicant.refuse.reason"].search_count(
        [("name", "=", REFUSE_REASON)]
    ) == 1, "Expected exactly one 'Not a fit' refuse reason"

    env.cr.commit()
