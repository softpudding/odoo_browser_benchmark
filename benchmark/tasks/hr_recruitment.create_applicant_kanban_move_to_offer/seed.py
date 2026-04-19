"""Seed for hr_recruitment.create_applicant_kanban_move_to_offer.

Category: deep_ui_interaction (MEDIUM).

Seeds a single job position 'Bench Senior Dev' scoped to the
'Bench Engineering' department, plus four recruitment stages named
(in order) 'Initial Qualification', 'Qualified', 'Contract Proposal',
'Contract Signed'. Each stage is explicitly linked to the new job via
the m2m 'job_ids' so the Applications kanban on that job only shows
these four columns (other shared stages from the demo data remain
untouched but are filtered out once job_ids is non-empty for our stages
— see note on stage scoping below).

No applicants are pre-created: the benchmark task asks the agent to
CREATE a new applicant through the kanban '+ New' quick-create in the
first column, fill contact details on the form, then move the card
through Qualified → Contract Proposal.

Calibration risks:
- Default recruitment stages in the demo data are named 'New',
  'Qualification', 'First Interview', 'Second Interview',
  'Contract Proposal', 'Contract Signed' (sequences 0..5). The spec
  asks for 'Initial Qualification' / 'Qualified' — NOT the default
  names — so this seed creates dedicated stages named exactly as the
  prompt states and attaches them to the new job.
- `hr.recruitment.stage.job_ids` defaults to [] which means a stage is
  visible to all jobs. Filling job_ids on our four stages scopes them
  to Bench Senior Dev so the agent sees exactly four columns.
- The kanban drag vs. status-bar-click are both offered in the prompt
  so browser-use has a fallback path if drag-and-drop fails.
"""

JOB_NAME = "Bench Senior Dev"
DEPARTMENT_NAME = "Bench Engineering"
APPLICANT_NAME = "Alice Applicant"

STAGE_SEQUENCE = [
    ("Initial Qualification", 10),
    ("Qualified", 20),
    ("Contract Proposal", 30),
    ("Contract Signed", 40),
]


def _ensure_department(env, name):
    dept = env["hr.department"].search([("name", "=", name)], limit=1)
    if not dept:
        dept = env["hr.department"].create({"name": name})
    return dept


def _cleanup_applicants(env):
    """Drop any applicant left over from prior runs, plus their chatter."""
    Applicant = env["hr.applicant"].with_context(active_test=False)
    old = Applicant.search([
        "|",
        ("partner_name", "=", APPLICANT_NAME),
        ("email_from", "=", "alice@bench.test"),
    ])
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
        # Orphan any applicants still linked to this job (safety)
        env["hr.applicant"].with_context(active_test=False).search([
            ("job_id", "=", job.id),
        ]).unlink()
        # Detach our canonical stages from this job; if a stage ends up
        # orphaned AND its name is one of our canonical set, drop it.
        our_names = [n for n, _ in STAGE_SEQUENCE]
        stages = env["hr.recruitment.stage"].with_context(
            active_test=False
        ).search([("job_ids", "in", [job.id])])
        for stage in stages:
            stage.write({"job_ids": [(3, job.id)]})
            if not stage.job_ids and stage.name in our_names:
                stage.unlink()
        job.unlink()

    # Also purge any orphan canonical stages (not linked to any job) whose
    # names collide with ours, to avoid them being re-attached wrongly.
    for sname, _ in STAGE_SEQUENCE:
        orphans = env["hr.recruitment.stage"].with_context(
            active_test=False
        ).search([("name", "=", sname)])
        for s in orphans:
            # Only drop if not tied to any job AND not a built-in demo
            # record (demo records set external ids, we won't).
            if not s.job_ids:
                # Safety: do not drop stages that are referenced by active
                # applicants (would ondelete='restrict').
                refs = env["hr.applicant"].with_context(
                    active_test=False
                ).search_count([("stage_id", "=", s.id)])
                if refs == 0:
                    s.unlink()


def setup(env):
    # 1. Cleanup in child-first order
    _cleanup_applicants(env)
    _cleanup_job_and_stages(env)

    # 2. Ensure department
    dept = _ensure_department(env, DEPARTMENT_NAME)

    # 3. Create the job (active, open for recruitment)
    job = env["hr.job"].create({
        "name": JOB_NAME,
        "department_id": dept.id,
        "no_of_recruitment": 1,
    })

    # 4. Create the four stages scoped to this job. Explicit sequence so
    #    the kanban grouping order is deterministic.
    for sname, seq in STAGE_SEQUENCE:
        env["hr.recruitment.stage"].create({
            "name": sname,
            "sequence": seq,
            "job_ids": [(6, 0, [job.id])],
        })

    # Sanity: no applicant named Alice Applicant on this job yet.
    assert not env["hr.applicant"].with_context(active_test=False).search([
        ("partner_name", "=", APPLICANT_NAME),
        ("job_id", "=", job.id),
    ]), f"Unexpected pre-existing applicant on {JOB_NAME}"

    env.cr.commit()
