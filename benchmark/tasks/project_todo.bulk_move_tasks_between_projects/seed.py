"""Seed for project_todo.bulk_move_tasks_between_projects.

HARD (tier 3). Task assigns 3 of 4 tasks from project A to project B via
project.task form edit; the 4th task (Delta) is a distractor that must
stay put. There is NO dedicated 'Move to Project' bulk action in Odoo 19
Community — `project_id` column on the task list view is read-only
(`<field name="project_id" ... readonly="1"/>` in
`project.project_task_view_tree_main_base`). Realistic reassignment path
is: open each task in form view, change `project_id` and save.

Seeded state:
  - project.project 'Bench Proj A' — 4 active tasks (Alpha, Bravo, Charlie, Delta)
  - project.project 'Bench Proj B' — zero tasks
"""

PROJECT_A = "Bench Proj A"
PROJECT_B = "Bench Proj B"

TASK_ALPHA = "Bench Task Alpha"
TASK_BRAVO = "Bench Task Bravo"
TASK_CHARLIE = "Bench Task Charlie"
TASK_DELTA = "Bench Task Delta"

ALL_TASK_NAMES = [TASK_ALPHA, TASK_BRAVO, TASK_CHARLIE, TASK_DELTA]
ALL_PROJECT_NAMES = [PROJECT_A, PROJECT_B]


def setup(env):
    # --- Cleanup prior runs ---
    env["project.task"].with_context(active_test=False).search([
        ("name", "in", ALL_TASK_NAMES),
    ]).unlink()

    old_projects = env["project.project"].with_context(active_test=False).search([
        ("name", "in", ALL_PROJECT_NAMES),
    ])
    for p in old_projects:
        env["project.task"].with_context(active_test=False).search([
            ("project_id", "=", p.id),
        ]).unlink()
    old_projects.unlink()

    # --- Create the two fresh projects ---
    proj_a = env["project.project"].create({"name": PROJECT_A})
    proj_b = env["project.project"].create({"name": PROJECT_B})

    # --- Create four tasks in A, B stays empty ---
    for name in ALL_TASK_NAMES:
        env["project.task"].create({
            "name": name,
            "project_id": proj_a.id,
        })

    # Sanity assertions the seed-status line can reflect.
    a_tasks = env["project.task"].search([("project_id", "=", proj_a.id)])
    b_tasks = env["project.task"].search([("project_id", "=", proj_b.id)])
    assert len(a_tasks) == 4, (
        f"seed: expected 4 tasks in {PROJECT_A}, got {len(a_tasks)}"
    )
    assert len(b_tasks) == 0, (
        f"seed: expected 0 tasks in {PROJECT_B}, got {len(b_tasks)}"
    )
