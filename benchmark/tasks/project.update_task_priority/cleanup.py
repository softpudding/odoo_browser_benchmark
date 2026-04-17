"""Clean up artifacts from previous runs."""


def cleanup(env):
    project = env["project.project"].search([("name", "=", "Astra Feature Rollout")])
    if project:
        env["project.task"].search([("project_id", "in", project.ids)]).unlink()
        project.unlink()
