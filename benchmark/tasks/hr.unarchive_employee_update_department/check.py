"""Postcondition checks for hr.unarchive_employee_update_department.

Validates:
1. Employee "Avery Collins" is now active (active=True).
2. Their department is set to "Engineering".
3. Their name/email are unchanged from the seed.
4. Distractor employee "Priya Patel" is untouched.
"""


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
