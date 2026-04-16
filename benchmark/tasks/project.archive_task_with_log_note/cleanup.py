"""Clean up artifacts from previous runs."""


def cleanup(env):
    project = env["project.project"].search(
        [("name", "=", "Nexus Platform Launch")], limit=1
    )
    if not project:
        return
    tasks = env["project.task"].with_context(active_test=False).search([
        ("project_id", "=", project.id),
    ])
    for task in tasks:
        env["mail.message"].search([
            ("model", "=", "project.task"),
            ("res_id", "=", task.id),
            ("subtype_id.name", "=", "Note"),
        ]).unlink()
    tasks.unlink()
    project.unlink()
