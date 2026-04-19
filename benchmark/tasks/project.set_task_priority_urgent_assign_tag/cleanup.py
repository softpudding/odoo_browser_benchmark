"""Cleanup for project.set_task_priority_urgent_assign_tag."""


PROJECT_NAME = "Bench Prio Project"
TASK_NAME = "Fix critical bug"
TAG_NAME = "Bug"


def cleanup(env):
    # Drop the task (by canonical name).
    env["project.task"].with_context(active_test=False).search([
        ("name", "=", TASK_NAME),
    ]).unlink()

    # Drop the project (any residual tasks first).
    project = env["project.project"].with_context(active_test=False).search([
        ("name", "=", PROJECT_NAME),
    ])
    for p in project:
        env["project.task"].with_context(active_test=False).search([
            ("project_id", "=", p.id),
        ]).unlink()
    project.unlink()

    # Drop the benchmark-owned tag.
    env["project.tags"].with_context(active_test=False).search([
        ("name", "=", TAG_NAME),
    ]).unlink()
