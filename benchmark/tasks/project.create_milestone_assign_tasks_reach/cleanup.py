"""Clean up artifacts created by project.create_milestone_assign_tasks_reach."""


PROJECT_NAME = "Bench Milestone Proj"

TASK_T1 = "T1 - Draft Spec"
TASK_T2 = "T2 - Build Prototype"
TASK_T3 = "T3 - Review Final"

ALL_TASK_NAMES = [TASK_T1, TASK_T2, TASK_T3]


def cleanup(env):
    env["project.task"].with_context(active_test=False).search([
        ("name", "in", ALL_TASK_NAMES),
    ]).unlink()

    project = env["project.project"].with_context(active_test=False).search([
        ("name", "=", PROJECT_NAME),
    ])
    for p in project:
        env["project.milestone"].search([("project_id", "=", p.id)]).unlink()
        env["project.task"].with_context(active_test=False).search([
            ("project_id", "=", p.id),
        ]).unlink()
    project.unlink()
