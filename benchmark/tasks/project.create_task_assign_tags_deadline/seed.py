"""Seed a project for the create-task-assign-stage task.

Category 2 (MEDIUM): Create a task with multiple fields (assignee,
deadline, priority, description) in a specific kanban stage. Browser-use
may miss some fields or place the task in the wrong stage.
"""

PROJECT_NAME = "Omega Platform Launch"
TASK_NAME = "Design Landing Page Mockup"


def setup(env):
    # --- Cleanup prior runs ---
    old_tasks = env["project.task"].search([("name", "=", TASK_NAME)])
    old_tasks.unlink()

    # --- Ensure project exists with stages ---
    project = env["project.project"].search(
        [("name", "=", PROJECT_NAME)], limit=1
    )
    if not project:
        project = env["project.project"].create({
            "name": PROJECT_NAME,
        })

    # Ensure "In Progress" stage exists for this project
    stage_names = ["To Do", "In Progress", "Done"]
    for idx, sname in enumerate(stage_names):
        stage = env["project.task.type"].search(
            [("name", "=", sname), ("project_ids", "in", [project.id])],
            limit=1,
        )
        if not stage:
            # Check if stage exists globally
            stage = env["project.task.type"].search(
                [("name", "=", sname)], limit=1
            )
            if stage:
                stage.write({"project_ids": [(4, project.id)]})
            else:
                env["project.task.type"].create({
                    "name": sname,
                    "sequence": (idx + 1) * 10,
                    "project_ids": [(4, project.id)],
                })

    # --- Create a few existing tasks so the project isn't empty ---
    in_progress = env["project.task.type"].search(
        [("name", "=", "In Progress"), ("project_ids", "in", [project.id])],
        limit=1,
    )
    todo = env["project.task.type"].search(
        [("name", "=", "To Do"), ("project_ids", "in", [project.id])],
        limit=1,
    )

    existing_tasks = [
        ("Set up CI/CD pipeline", todo.id if todo else False),
        ("Write API integration spec", in_progress.id if in_progress else False),
    ]
    for tname, stage_id in existing_tasks:
        if not env["project.task"].search([
            ("name", "=", tname),
            ("project_id", "=", project.id),
        ], limit=1):
            env["project.task"].create({
                "name": tname,
                "project_id": project.id,
                "stage_id": stage_id,
            })
