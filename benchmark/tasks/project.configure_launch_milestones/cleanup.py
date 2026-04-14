"""Clean up artifacts from previous runs."""


def cleanup(env):
    project = env["project.project"].search([("name", "=", "Atlas Redesign")], limit=1)
    if project:
        env["project.task"].search([("project_id", "=", project.id)]).unlink()
        env["project.milestone"].search([("project_id", "=", project.id)]).unlink()
        project.write({
            "allow_milestones": False,
            "description": False,
        })


