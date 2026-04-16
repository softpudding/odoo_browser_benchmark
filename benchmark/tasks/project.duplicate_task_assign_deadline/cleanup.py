"""Cleanup for project.duplicate_task_assign_deadline."""


def cleanup(env):
    project = env["project.project"].search([("name", "=", "Launch Enablement Board")], limit=1)
    if not project:
        return
    env["project.task"].with_context(active_test=False).search([
        ("project_id", "=", project.id),
        ("name", "in", [
            "Prepare webinar outline",
            "Prepare webinar outline - APAC",
            "Prepare sales deck",
        ]),
    ]).unlink()
