"""Clean up artifacts from previous runs."""


def cleanup(env):
    employee = env["hr.employee"].search([("name", "=", "Sofia Chen")], limit=1)
    if employee:
        employee.write({"work_phone": "+1 555 0200"})
