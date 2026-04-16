"""Clean up artifacts from previous runs."""


def cleanup(env):
    project = env["project.project"].search(
        [("name", "=", "Atlas Support Rollout")],
        limit=1,
    )
    if not project:
        return

    tasks = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "in", [
            "Vendor readiness checklist",
            "Launch coordination",
            "Archived coordination notes",
        ]),
    ])
    tasks.unlink()
