"""Postcondition checks for hr.schedule_employee_activity.

Validates that:
1. A Call activity exists for Sofia Chen with due date 2026-05-10
2. The activity summary is "Annual review discussion"
"""


def check(env):
    failures = []

    # Find the employee
    employee = env["hr.employee"].search([
        ("name", "=", "Sofia Chen"),
    ], limit=1)

    if not employee:
        return ["Employee 'Sofia Chen' not found"]

    # Find activities for this employee
    activities = env["mail.activity"].search([
        ("res_model", "=", "hr.employee"),
        ("res_id", "=", employee.id),
    ])

    if not activities:
        return ["No activities found for employee 'Sofia Chen'"]

    # Find a Call activity with the correct due date and summary
    found = False
    for activity in activities:
        if (activity.activity_type_id.name == "Call"
                and str(activity.date_deadline) == "2026-05-10"
                and activity.summary == "Annual review discussion"):
            found = True
            break

    if not found:
        activity_details = ", ".join(
            f"type={a.activity_type_id.name}, date={a.date_deadline}, summary={a.summary}"
            for a in activities
        )
        failures.append(
            f"No Call activity with date '2026-05-10' and summary 'Annual review discussion' found. "
            f"Found: {activity_details}"
        )

    return failures