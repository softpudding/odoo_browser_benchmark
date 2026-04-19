"""Cleanup for project.close_task_change_state_to_done."""


PROJECT_NAME = "Bench Close Project"
TASK_NAME = "Review document"


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
