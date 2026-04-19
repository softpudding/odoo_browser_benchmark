"""Cleanup for project.complete_project_stage_reach_done_percent."""


PROJECT_NAME = "Bench Progress Project"
TASK_NAMES = ["Task A", "Task B", "Task C"]


def cleanup(env):
    # Drop tasks by canonical name.
    env["project.task"].with_context(active_test=False).search([
        ("name", "in", TASK_NAMES),
    ]).unlink()

    # Drop the project (cascade-delete residual tasks first).
    project = env["project.project"].with_context(active_test=False).search([
        ("name", "=", PROJECT_NAME),
    ])
    for p in project:
        env["project.task"].with_context(active_test=False).search([
            ("project_id", "=", p.id),
        ]).unlink()
        # Unlink stages scoped only to this project (m2m); leave globally
        # shared stages alone.
        stages_scoped = env["project.task.type"].with_context(active_test=False).search([
            ("project_ids", "in", [p.id]),
        ])
        for stage in stages_scoped:
            stage.write({"project_ids": [(3, p.id)]})
    project.unlink()
