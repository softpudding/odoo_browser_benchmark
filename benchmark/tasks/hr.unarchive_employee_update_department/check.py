"""Postcondition checks for hr.unarchive_employee_update_department.

Validates:
1. Employee "Avery Collins" is now active (active=True).
2. Their department is set to "Engineering".
3. Their work location is set to "Home".
4. They have one exact Call activity scheduled.
5. Their name/email are unchanged from the seed.
6. Distractor employee "Priya Patel" is untouched.
"""

from datetime import date


def check(env):
    failures = []

    Emp = env["hr.employee"].with_context(active_test=False)

    target = Emp.search([("name", "=", "Avery Collins")], limit=1)
    if not target:
        return ["Employee 'Avery Collins' not found"]

    if not target.active:
        failures.append("Employee 'Avery Collins' is still archived")

    if not target.department_id or target.department_id.name != "Engineering":
        dept_name = target.department_id.name if target.department_id else None
        failures.append(
            f"Department is '{dept_name}', expected 'Engineering'"
        )

    if not target.work_location_id or target.work_location_id.name != "Home":
        loc_name = target.work_location_id.name if target.work_location_id else None
        failures.append(
            f"Work Location is '{loc_name}', expected 'Home'"
        )

    activities = env["mail.activity"].search([
        ("res_model", "=", "hr.employee"),
        ("res_id", "=", target.id),
        ("summary", "=", "Complete reactivation checklist"),
    ])
    if len(activities) != 1:
        failures.append(
            f"Expected exactly 1 matching activity, found {len(activities)}"
        )
    else:
        activity = activities[0]
        if activity.activity_type_id.name != "Call":
            failures.append(
                f"Activity type is '{activity.activity_type_id.name}', expected 'Call'"
            )
        if activity.date_deadline != date(2026, 5, 21):
            failures.append(
                f"Activity due date is {activity.date_deadline}, expected 2026-05-21"
            )

    if target.work_email != "avery.collins@example.com":
        failures.append(
            f"Work email was changed to '{target.work_email}'"
        )

    distractor = Emp.search([("name", "=", "Priya Patel")], limit=1)
    if not distractor:
        failures.append("Distractor employee 'Priya Patel' is missing")
    else:
        if not distractor.active:
            failures.append("Distractor 'Priya Patel' was archived")
        if not distractor.department_id or distractor.department_id.name != "Engineering":
            failures.append(
                "Distractor 'Priya Patel' department changed from Engineering"
            )

    return failures
