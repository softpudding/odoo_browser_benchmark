"""Clean up artifacts from previous runs."""


def cleanup(env):
    employee = env["hr.employee"].search([("name", "=", "Sofia Chen")], limit=1)
    if employee:
        env["mail.activity"].search([
            ("res_model", "=", "hr.employee"),
            ("res_id", "=", employee.id),
        ]).unlink()