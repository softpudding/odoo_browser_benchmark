"""Cleanup for project_todo.bulk_move_tasks_between_projects."""


PROJECT_A = "Bench Proj A"
PROJECT_B = "Bench Proj B"

ALL_TASK_NAMES = [
    "Bench Task Alpha",
    "Bench Task Bravo",
    "Bench Task Charlie",
    "Bench Task Delta",
]
ALL_PROJECT_NAMES = [PROJECT_A, PROJECT_B]


def cleanup(env):
    env["project.task"].with_context(active_test=False).search([
        ("name", "in", ALL_TASK_NAMES),
    ]).unlink()

    projects = env["project.project"].with_context(active_test=False).search([
        ("name", "in", ALL_PROJECT_NAMES),
    ])
    for p in projects:
        env["project.task"].with_context(active_test=False).search([
            ("project_id", "=", p.id),
        ]).unlink()
    projects.unlink()
