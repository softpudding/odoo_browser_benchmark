"""Postcondition checks for hr_recruitment.create_applicant_kanban_move_to_offer.

Validates:
1. Exactly one hr.applicant with partner_name='Alice Applicant' exists
   on the 'Bench Senior Dev' job.
2. Her email_from is exactly 'alice@bench.test'.
3. Her partner_phone is exactly '+15555555555'.
4. Her stage_id is the 'Contract Proposal' stage scoped to this job.
5. She is still active (not archived, not refused).
6. The four canonical stages are still present and linked to the job
   (no rename/delete).
"""

JOB_NAME = "Bench Senior Dev"
APPLICANT_NAME = "Alice Applicant"
EXPECTED_EMAIL = "alice@bench.test"
EXPECTED_PHONE = "+15555555555"
TARGET_STAGE = "Contract Proposal"
EXPECTED_STAGES = [
    "Initial Qualification",
    "Qualified",
    "Contract Proposal",
    "Contract Signed",
]


def _norm_phone(p):
    if not p:
        return ""
    # Collapse whitespace, remove common separators to allow for minor
    # UI-side reformatting; the prompt explicitly forbids spaces/dashes
    # but some phone widgets normalise via libphonenumber — accept only
    # the canonical form.
    return p.replace(" ", "").replace("-", "").replace("\u00a0", "")


def check(env):
    failures = []

    job = env["hr.job"].with_context(active_test=False).search(
        [("name", "=", JOB_NAME)], limit=1
    )
    if not job:
        return [f"Job '{JOB_NAME}' not found"]

    # Applicants on this job
    applicants = env["hr.applicant"].with_context(active_test=False).search([
        ("job_id", "=", job.id),
    ])
    alice = applicants.filtered(lambda a: a.partner_name == APPLICANT_NAME)

    if not alice:
        return [
            f"No applicant with partner_name='{APPLICANT_NAME}' on job "
            f"'{JOB_NAME}' (found {applicants.mapped('partner_name')})"
        ]
    if len(alice) > 1:
        failures.append(
            f"Found {len(alice)} applicants named '{APPLICANT_NAME}' on "
            f"'{JOB_NAME}' — expected exactly 1"
        )

    alice = alice[:1]

    # --- email ---
    if (alice.email_from or "").strip() != EXPECTED_EMAIL:
        failures.append(
            f"Applicant email_from is {alice.email_from!r}; "
            f"expected {EXPECTED_EMAIL!r}"
        )

    # --- phone ---
    if _norm_phone(alice.partner_phone) != EXPECTED_PHONE:
        failures.append(
            f"Applicant partner_phone is {alice.partner_phone!r}; "
            f"expected {EXPECTED_PHONE!r}"
        )

    # --- stage ---
    if not alice.stage_id:
        failures.append("Applicant has no stage_id set")
    elif alice.stage_id.name != TARGET_STAGE:
        failures.append(
            f"Applicant stage is '{alice.stage_id.name}'; expected "
            f"'{TARGET_STAGE}'"
        )
    elif job.id not in alice.stage_id.job_ids.ids:
        failures.append(
            f"Applicant stage '{TARGET_STAGE}' is not scoped to job "
            f"'{JOB_NAME}' (job_ids={alice.stage_id.job_ids.mapped('name')})"
        )

    # --- active / not refused ---
    if not alice.active:
        failures.append("Applicant should be active (not archived)")
    if alice.refuse_reason_id:
        failures.append(
            f"Applicant should not be refused (refuse_reason_id="
            f"{alice.refuse_reason_id.name})"
        )
    if alice.date_closed:
        failures.append(
            "Applicant date_closed is set — applicant must not have been "
            "moved to a hired_stage"
        )

    # --- seed stages still intact ---
    for sname in EXPECTED_STAGES:
        stage = env["hr.recruitment.stage"].with_context(
            active_test=False
        ).search([
            ("name", "=", sname),
            ("job_ids", "in", [job.id]),
        ], limit=1)
        if not stage:
            failures.append(
                f"Seeded stage '{sname}' missing from job '{JOB_NAME}' "
                "(do not rename or delete stages)"
            )

    return failures
