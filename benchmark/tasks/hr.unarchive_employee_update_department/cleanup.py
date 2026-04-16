"""Clean up artifacts from previous runs."""


def cleanup(env):
    Emp = env["hr.employee"].with_context(active_test=False)
    Emp.search([
        ("name", "in", ["Avery Collins", "Priya Patel"]),
    ]).unlink()
