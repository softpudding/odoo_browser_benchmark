"""Clean up artifacts from previous runs."""


def cleanup(env):
    project = env["project.project"].search([("name", "=", "Omega Platform Launch")])
    for proj in project:
        proj.task_ids.unlink()
    project.unlink()
