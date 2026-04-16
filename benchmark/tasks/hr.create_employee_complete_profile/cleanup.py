"""Clean up artifacts from previous runs."""


def cleanup(env):
    employees = env["hr.employee"].search([("name", "=", "Jordan Mercer")])
    employees.unlink()
