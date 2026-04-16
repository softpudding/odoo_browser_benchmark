"""Seed a medium project-subtask workflow."""

PROJECT_NAME = "Atlas Implementation Sprint"
PARENT_TASK = "Prepare onboarding checklist"
SUBTASK_NAME = "Draft kickoff agenda"
DISTRACTOR_TASK = "Review onboarding checklist"


def _ensure_stage(env, project, name, sequence):
    stage = env["project.task.type"].search([
        ("name", "=", name),
        ("project_ids", "in", [project.id]),
    ], limit=1)
    if stage:
        return stage
    stage = env["project.task.type"].search([("name", "=", name)], limit=1)
    if stage:
        stage.write({"project_ids": [(4, project.id)]})
        return stage
    return env["project.task.type"].create({
        "name": name,
        "sequence": sequence,
        "project_ids": [(4, project.id)],
    })


def setup(env):
    env["project.project"].search([("name", "=", PROJECT_NAME)]).unlink()

    project = env["project.project"].create({
        "name": PROJECT_NAME,
    })

    stage_todo = _ensure_stage(env, project, "To Do", 10)
    stage_in_progress = _ensure_stage(env, project, "In Progress", 20)
    project.write({"type_ids": [(6, 0, [stage_todo.id, stage_in_progress.id])]})

    env["project.task"].create({
        "name": PARENT_TASK,
        "project_id": project.id,
        "stage_id": stage_todo.id,
        "description": "Collect the onboarding steps before the kickoff call.",
        "user_ids": [(5, 0, 0)],
    })
    env["project.task"].create({
        "name": DISTRACTOR_TASK,
        "project_id": project.id,
        "stage_id": stage_todo.id,
        "description": "Leave this distractor task untouched.",
        "user_ids": [(5, 0, 0)],
    })
