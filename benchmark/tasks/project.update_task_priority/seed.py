"""Seed a project task for the task-priority update workflow."""

PROJECT_NAME = "Astra Feature Rollout"
TASK_NAME = "Validate release notes"


def setup(env):
    # --- Cleanup prior runs ---
    old_project = env["project.project"].search([("name", "=", PROJECT_NAME)])
    if old_project:
        for task in env["project.task"].search([("project_id", "in", old_project.ids)]):
            task.unlink()
        old_project.unlink()

    env["project.task"].search([("name", "=", TASK_NAME)]).unlink()

    # --- Create project ---
    project = env["project.project"].create({"name": PROJECT_NAME})

    # --- Ensure stages ---
    stage_names = ["To Do", "In Progress", "Done"]
    stage_map = {}
    for idx, sname in enumerate(stage_names):
        stage = env["project.task.type"].search([
            ("name", "=", sname),
            ("project_ids", "in", [project.id]),
        ], limit=1)
        if not stage:
            existing = env["project.task.type"].search([("name", "=", sname)], limit=1)
            if existing:
                existing.write({"project_ids": [(4, project.id)]})
                stage = existing
            else:
                stage = env["project.task.type"].create({
                    "name": sname,
                    "sequence": (idx + 1) * 10,
                    "project_ids": [(4, project.id)],
                })
        stage_map[sname] = stage

    # --- Seed task with normal priority ---
    env["project.task"].create({
        "name": TASK_NAME,
        "project_id": project.id,
        "priority": "0",
        "stage_id": stage_map["To Do"].id,
        "description": "Cross-check release checklist and merge readiness items.",
    })
