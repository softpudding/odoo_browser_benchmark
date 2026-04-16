"""Clean up artifacts from previous runs."""


def cleanup(env):
    project = env["project.project"].search(
        [("name", "=", "Operations Knowledge Base")],
        limit=1,
    )
    if not project:
        return

    env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "in", [
            "Draft launch checklist",
            "Draft launch checklist follow-up",
            "Draft launch checklist mobile",
        ]),
    ]).unlink()
