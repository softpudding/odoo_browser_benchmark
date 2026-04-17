"""Seed a project with two kanban tasks both in the 'To Do' stage.

Category: deep_ui_interaction (EASY).

Capability tested: Kanban drag-and-drop. The agent must drag the task
'Benchmark Card Alpha' from the 'To Do' column to the 'In Progress'
column. A drag gesture is a UI pattern not otherwise exercised by the
suite.
"""

PROJECT_NAME = "Benchmark Drag Project"
ALPHA_NAME = "Benchmark Card Alpha"
BETA_NAME = "Benchmark Card Beta"
STAGE_SEQUENCE = [("To Do", 1), ("In Progress", 2), ("Done", 3)]


def setup(env):
    # --- Cleanup prior runs ---
    old_tasks = env["project.task"].with_context(active_test=False).search([
        ("name", "in", [ALPHA_NAME, BETA_NAME]),
    ])
    old_tasks.unlink()

    old_project = env["project.project"].search(
        [("name", "=", PROJECT_NAME)], limit=1
    )
    if old_project:
        # Delete tasks still linked to the project (safety)
        env["project.task"].with_context(active_test=False).search([
            ("project_id", "=", old_project.id),
        ]).unlink()
        old_project.unlink()

    # --- Create fresh project ---
    project = env["project.project"].create({
        "name": PROJECT_NAME,
    })

    # --- Create the three stages and link them to this project ---
    # project.task.type uses project_ids (m2m) to link stages to projects.
    stages_by_name = {}
    for sname, seq in STAGE_SEQUENCE:
        # Try to reuse an existing stage already linked to this project
        stage = env["project.task.type"].search([
            ("name", "=", sname),
            ("project_ids", "in", [project.id]),
        ], limit=1)
        if not stage:
            # Create a fresh stage scoped just to this project so the
            # sequence we set is authoritative for the kanban grouping.
            stage = env["project.task.type"].create({
                "name": sname,
                "sequence": seq,
                "project_ids": [(6, 0, [project.id])],
            })
        stages_by_name[sname] = stage

    todo = stages_by_name["To Do"]

    # --- Create the two tasks, both starting in the 'To Do' column ---
    env["project.task"].create({
        "name": ALPHA_NAME,
        "project_id": project.id,
        "stage_id": todo.id,
    })
    env["project.task"].create({
        "name": BETA_NAME,
        "project_id": project.id,
        "stage_id": todo.id,
    })
