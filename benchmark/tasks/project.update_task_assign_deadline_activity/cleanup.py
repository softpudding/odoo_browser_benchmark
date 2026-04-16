"""Clean up artifacts from previous runs."""


def cleanup(env):
    env["mail.activity"].search([("summary", "=", "Review FAQ revisions")]).unlink()

    project = env["project.project"].search(
        [("name", "=", "Customer Portal Refresh")], limit=1
    )
    if not project:
        return

    env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "in", ["Revise FAQ copy", "Revise API docs"]),
    ]).unlink()
