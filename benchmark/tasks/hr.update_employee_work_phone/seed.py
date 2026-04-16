"""Seed an employee for the work-phone update task."""


def setup(env):
    employee = env["hr.employee"].search([("name", "=", "Sofia Chen")], limit=1)
    if not employee:
        env["hr.employee"].create({
            "name": "Sofia Chen",
            "work_email": "sofia.chen@example.com",
            "work_phone": "+1 555 0200",
        })
    else:
        employee.write({
            "work_email": "sofia.chen@example.com",
            "work_phone": "+1 555 0200",
        })
