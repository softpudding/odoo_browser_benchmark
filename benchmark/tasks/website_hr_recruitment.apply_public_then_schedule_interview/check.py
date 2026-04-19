"""Postcondition checks for website_hr_recruitment.apply_public_then_schedule_interview.

Validates:
  1. Exactly 1 hr.applicant named 'Bench Candidate' for 'Senior Backend Engineer'
     with the expected email (Phase 1 public submission).
  2. Exactly 1 Meeting/Interview mail.activity scheduled on that applicant
     with date_deadline 2026-05-04 (Phase 2 back-office scheduling).
"""

from datetime import date

JOB_NAME = "Senior Backend Engineer"
APPLICANT_NAME = "Bench Candidate"
APPLICANT_EMAIL = "bench.candidate@example.com"
ACTIVITY_SUMMARY = "Interview"
ACTIVITY_DUE_DATE = date(2026, 5, 4)


def check(env):
    failures = []

    # ----- Job exists and is published -----
    job = env["hr.job"].with_context(active_test=False).search(
        [("name", "=", JOB_NAME)], limit=1
    )
    if not job:
        return [f"Job '{JOB_NAME}' not found — seed may have failed"]
    if not job.is_published:
        failures.append(f"Job '{JOB_NAME}' is not published")

    # ----- Applicant exists with expected fields -----
    applicants = env["hr.applicant"].with_context(active_test=False).search([
        ("partner_name", "=", APPLICANT_NAME),
    ])
    if not applicants:
        return [f"Applicant '{APPLICANT_NAME}' not found — Phase 1 was not completed"]
    if len(applicants) > 1:
        failures.append(
            f"Expected exactly 1 applicant named '{APPLICANT_NAME}', "
            f"found {len(applicants)}"
        )
    applicant = applicants[0]

    if applicant.job_id.id != job.id:
        failures.append(
            f"Applicant '{APPLICANT_NAME}' is linked to job "
            f"'{applicant.job_id.name}', expected '{JOB_NAME}'"
        )

    if (applicant.email_from or "").strip().lower() != APPLICANT_EMAIL.lower():
        failures.append(
            f"Applicant email_from is '{applicant.email_from}', "
            f"expected '{APPLICANT_EMAIL}'"
        )

    # ----- Activity validation -----
    activities = env["mail.activity"].search([
        ("res_model", "=", "hr.applicant"),
        ("res_id", "=", applicant.id),
    ])
    if not activities:
        failures.append(
            f"No mail.activity found on applicant '{APPLICANT_NAME}' — "
            f"expected a 'Meeting' activity with summary 'Interview'"
        )
    else:
        # Filter activities whose summary matches 'Interview' (case-insensitive).
        matching = activities.filtered(
            lambda a: (a.summary or "").strip().lower() == ACTIVITY_SUMMARY.lower()
        )
        if not matching:
            summaries = ", ".join(a.summary or "(empty)" for a in activities)
            failures.append(
                f"No activity with summary '{ACTIVITY_SUMMARY}' found. "
                f"Existing summaries: [{summaries}]"
            )
        elif len(matching) > 1:
            failures.append(
                f"Expected exactly 1 activity with summary '{ACTIVITY_SUMMARY}', "
                f"found {len(matching)}"
            )
        else:
            act = matching[0]
            if act.date_deadline != ACTIVITY_DUE_DATE:
                failures.append(
                    f"Activity due date is {act.date_deadline}, "
                    f"expected {ACTIVITY_DUE_DATE}"
                )
            # Accept either a "Meeting" type OR no type set (some agents forget
            # to change the default); the summary + date + presence are the
            # primary signal. But prompt says Meeting, so flag mismatches.
            meeting_type = env["mail.activity.type"].search(
                ["|", ("name", "=", "Meeting"), ("category", "=", "meeting")],
                limit=1,
            )
            if meeting_type and act.activity_type_id.id != meeting_type.id:
                failures.append(
                    f"Activity type is '{act.activity_type_id.name}', "
                    f"expected 'Meeting'"
                )

    # ----- No extras / deletions -----
    all_for_job = env["hr.applicant"].with_context(active_test=False).search([
        ("job_id", "=", job.id),
    ])
    if len(all_for_job) != 1:
        names = [a.partner_name for a in all_for_job]
        failures.append(
            f"Expected exactly 1 applicant for job '{JOB_NAME}', "
            f"found {len(all_for_job)}: {names}"
        )

    return failures
