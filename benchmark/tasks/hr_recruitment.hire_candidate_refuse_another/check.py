"""Postcondition checks for hr_recruitment.hire_candidate_refuse_another.

Validates:
1. 'Top Candidate' on 'Bench Role' is HIRED:
     - active=True
     - stage_id.hired_stage=True (i.e. moved to Contract Signed)
     - date_closed is set (the stage-hired trigger)
     - employee_id is set, pointing at a real hr.employee with the
       applicant's name linked back via applicant_ids.
2. 'Runner Up' on 'Bench Role' is REFUSED:
     - active=False
     - refuse_reason_id.name == 'Not a fit'
3. The Bench Role job still exists and no extra applicants have been
   created on it.
"""

JOB_NAME = "Bench Role"
TOP_NAME = "Top Candidate"
RUNNER_NAME = "Runner Up"
REFUSE_REASON = "Not a fit"
EMPLOYEE_JOB_TITLE = "Bench Role (Hired)"


def check(env):
    failures = []
    Applicant = env["hr.applicant"].with_context(active_test=False)

    job = env["hr.job"].with_context(active_test=False).search(
        [("name", "=", JOB_NAME)], limit=1
    )
    if not job:
        return [f"Job '{JOB_NAME}' not found"]

    top = Applicant.search([
        ("partner_name", "=", TOP_NAME),
        ("job_id", "=", job.id),
    ], limit=1)
    runner = Applicant.search([
        ("partner_name", "=", RUNNER_NAME),
        ("job_id", "=", job.id),
    ], limit=1)

    if not top:
        failures.append(f"Applicant '{TOP_NAME}' on '{JOB_NAME}' not found")
    if not runner:
        failures.append(f"Applicant '{RUNNER_NAME}' on '{JOB_NAME}' not found")

    # --- Top Candidate must be HIRED ---
    if top:
        if not top.active:
            failures.append(
                f"'{TOP_NAME}' should still be active (hired, not archived)"
            )
        if top.refuse_reason_id:
            failures.append(
                f"'{TOP_NAME}' was refused with reason "
                f"'{top.refuse_reason_id.name}' — should have been hired"
            )
        if not top.stage_id or not top.stage_id.hired_stage:
            failures.append(
                f"'{TOP_NAME}' stage '{top.stage_id.name if top.stage_id else None}'"
                f" is not a hired stage (hired_stage=True)"
            )
        if not top.date_closed:
            failures.append(
                f"'{TOP_NAME}' has no date_closed set — hire did not commit"
            )
        if not top.employee_id:
            failures.append(
                f"'{TOP_NAME}' has no employee_id — Create Employee was "
                "not clicked / saved"
            )
        else:
            emp = top.employee_id
            if not emp.exists():
                failures.append(
                    f"'{TOP_NAME}' employee_id points at a deleted record"
                )
            else:
                if emp.name != TOP_NAME:
                    failures.append(
                        f"Linked employee name is '{emp.name}'; expected "
                        f"'{TOP_NAME}'"
                    )
                if top not in emp.applicant_ids:
                    failures.append(
                        "Applicant -> Employee link not bidirectional "
                        "(employee.applicant_ids does not contain the applicant)"
                    )
                if (emp.job_title or "").strip() != EMPLOYEE_JOB_TITLE:
                    failures.append(
                        f"Employee job_title is {emp.job_title!r}, "
                        f"expected {EMPLOYEE_JOB_TITLE!r}"
                    )

    # --- Runner Up must be REFUSED with the right reason ---
    if runner:
        if runner.active:
            failures.append(
                f"'{RUNNER_NAME}' is still active — should be refused/archived"
            )
        if not runner.refuse_reason_id:
            failures.append(
                f"'{RUNNER_NAME}' has no refuse_reason_id — refuse wizard "
                "was not applied"
            )
        elif runner.refuse_reason_id.name != REFUSE_REASON:
            failures.append(
                f"'{RUNNER_NAME}' refuse reason is "
                f"'{runner.refuse_reason_id.name}', expected "
                f"'{REFUSE_REASON}'"
            )
        if runner.employee_id:
            failures.append(
                f"'{RUNNER_NAME}' unexpectedly has an employee_id set — "
                "must not be hired"
            )

    # --- No extra applicants on this job ---
    extras = Applicant.search([("job_id", "=", job.id)]) - (top | runner)
    if extras:
        failures.append(
            f"Unexpected extra applicants on '{JOB_NAME}': "
            f"{extras.mapped('partner_name')}"
        )

    # --- Refuse reason still present (do not rename/delete the seeded one) ---
    reason = env["hr.applicant.refuse.reason"].search(
        [("name", "=", REFUSE_REASON)], limit=1
    )
    if not reason:
        failures.append(
            f"Seeded refuse reason '{REFUSE_REASON}' is missing — do not "
            "rename or delete seeded reasons"
        )

    return failures
