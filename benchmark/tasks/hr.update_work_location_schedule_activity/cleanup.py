"""Clean up artifacts from previous runs."""


def cleanup(env):
    employee = env["hr.employee"].search([("name", "=", "Avery Collins")])
    if employee:
        env["mail.activity"].search([
            ("res_model", "=", "hr.employee"),
            ("res_id", "in", employee.ids),
        ]).unlink()
        employee.unlink()
