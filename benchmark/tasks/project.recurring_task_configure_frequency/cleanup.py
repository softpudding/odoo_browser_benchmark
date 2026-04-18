"""Clean up artifacts from previous runs of the recurring task workflow."""


PROJECT_NAME = "Bench Recurring Project"
TASK_NAME = "Weekly Status Update"


def cleanup(env):
    # Drop tasks (and their recurrences) bearing our seed name.
    tasks = env["project.task"].with_context(active_test=False).search([
        ("name", "=", TASK_NAME),
    ])
    if tasks:
        recurrences = tasks.mapped("recurrence_id")
        tasks.write({"recurring_task": False, "recurrence_id": False})
        if recurrences:
            recurrences.unlink()
        tasks.unlink()

    project = env["project.project"].with_context(active_test=False).search(
        [("name", "=", PROJECT_NAME)], limit=1
    )
    if project:
        leftover = env["project.task"].with_context(active_test=False).search([
            ("project_id", "=", project.id),
        ])
        if leftover:
            recurrences = leftover.mapped("recurrence_id")
            leftover.write({"recurring_task": False, "recurrence_id": False})
            if recurrences:
                recurrences.unlink()
            leftover.unlink()
        project.unlink()
