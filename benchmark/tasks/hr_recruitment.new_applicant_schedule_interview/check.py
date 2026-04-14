"""Postcondition checks for hr_recruitment.new_applicant_schedule_interview.

Validates:
1. Elena Vasquez applicant exists with correct field values
2. A "Call" activity is scheduled on the applicant with correct details
3. Distractor applicant Alex Kemp was not modified
4. No extra applicants were created for the job position
"""

from datetime import date


def check(env):
    failures = []

    # ------------------------------------------------------------------
    # 0. Prerequisite: Marc Demo must exist
    # ------------------------------------------------------------------
    marc = env["res.users"].search([("login", "=", "marc.demo")], limit=1)
    if not marc:
        failures.append("Marc Demo user (marc.demo) not found — seed may have failed")
        return failures

    # ------------------------------------------------------------------
    # 1. Find Elena Vasquez applicant
    # ------------------------------------------------------------------
    elena = env["hr.applicant"].search([
        ("partner_name", "=", "Elena Vasquez"),
    ])
    if len(elena) == 0:
        failures.append("Applicant 'Elena Vasquez' not found")
        return failures
    if len(elena) > 1:
        failures.append(
            f"Multiple applicants named 'Elena Vasquez' found ({len(elena)}), "
            f"expected exactly 1"
        )
        return failures

    elena = elena[0]

    # ------------------------------------------------------------------
    # 2. Validate applicant fields
    # ------------------------------------------------------------------
    if elena.email_from != "elena.vasquez@example.com":
        failures.append(
            f"Email is '{elena.email_from}', expected 'elena.vasquez@example.com'"
        )

    if elena.partner_phone != "+1 555-0142":
        phone = (elena.partner_phone or "").replace(" ", "").replace("-", "")
        expected = "+15550142"
        if phone != expected:
            failures.append(
                f"Phone is '{elena.partner_phone}', expected '+1 555-0142'"
            )

    if elena.salary_expected != 85000:
        failures.append(
            f"Expected salary is {elena.salary_expected}, expected 85000"
        )

    if elena.salary_expected_extra:
        failures.append(
            f"Extra salary advantage is '{elena.salary_expected_extra}', expected blank"
        )

    # Recruiter = Marc Demo
    if elena.user_id.id != marc.id:
        failures.append(
            f"Recruiter is '{elena.user_id.name or 'not set'}', expected 'Marc Demo'"
        )

    # Job position
    job = env["hr.job"].search([("name", "=", "Senior Backend Developer")], limit=1)
    if not job:
        failures.append("Job position 'Senior Backend Developer' not found")
    elif elena.job_id.id != job.id:
        failures.append(
            f"Applicant job is '{elena.job_id.name}', "
            f"expected 'Senior Backend Developer'"
        )

    # Stage = New
    new_stage = env["hr.recruitment.stage"].search([
        ("name", "ilike", "New"),
    ], limit=1)
    if new_stage and elena.stage_id.id != new_stage.id:
        failures.append(
            f"Stage is '{elena.stage_id.name}', expected 'New'"
        )

    # Evaluation = Normal (priority = '0')
    if elena.priority != '0':
        priority_labels = {'0': 'Normal', '1': 'Good', '2': 'Very Good', '3': 'Excellent'}
        failures.append(
            f"Evaluation is '{priority_labels.get(elena.priority, elena.priority)}', "
            f"expected 'Normal'"
        )

    # ------------------------------------------------------------------
    # 3. Validate scheduled activity
    # ------------------------------------------------------------------
    activities = env["mail.activity"].search([
        ("res_model", "=", "hr.applicant"),
        ("res_id", "=", elena.id),
    ])

    if not activities:
        failures.append(
            "No activity found on Elena Vasquez's applicant — "
            "expected a 'Call' activity scheduled for 2026-05-01"
        )
    else:
        call_type = env["mail.activity.type"].search([
            ("name", "ilike", "Call"),
        ], limit=1)

        call_activities = activities.filtered(
            lambda a: a.activity_type_id.id == call_type.id
        ) if call_type else env["mail.activity"]

        if not call_activities:
            type_names = ", ".join(a.activity_type_id.name for a in activities)
            failures.append(
                f"No 'Call' activity found on applicant. "
                f"Found activity types: [{type_names}]"
            )
        else:
            act = call_activities[0]

            # Due date
            expected_date = date(2026, 5, 1)
            if act.date_deadline != expected_date:
                failures.append(
                    f"Activity due date is {act.date_deadline}, "
                    f"expected {expected_date}"
                )

            # Assigned to Marc Demo
            if act.user_id.id != marc.id:
                failures.append(
                    f"Activity assigned to '{act.user_id.name}', "
                    f"expected 'Marc Demo'"
                )

            # Summary
            if not act.summary or "first technical interview" not in act.summary.lower():
                failures.append(
                    f"Activity summary is '{act.summary}', "
                    f"expected 'First technical interview'"
                )

    # ------------------------------------------------------------------
    # 4. Distractor applicant unchanged
    # ------------------------------------------------------------------
    alex = env["hr.applicant"].search([
        ("partner_name", "=", "Alex Kemp"),
    ], limit=1)
    if not alex:
        failures.append("Distractor applicant 'Alex Kemp' was deleted")
    else:
        if alex.email_from != "alex.kemp@example.com":
            failures.append(
                f"Distractor Alex Kemp email changed to '{alex.email_from}'"
            )
        if alex.salary_expected != 78000:
            failures.append(
                f"Distractor Alex Kemp salary changed to {alex.salary_expected}"
            )

    # ------------------------------------------------------------------
    # 5. No extra applicants for this job
    # ------------------------------------------------------------------
    if job:
        all_applicants = env["hr.applicant"].search([("job_id", "=", job.id)])
        if len(all_applicants) > 2:
            names = [a.partner_name for a in all_applicants]
            failures.append(
                f"Expected 2 applicants for the job, found {len(all_applicants)}: "
                f"{names}"
            )

    return failures
