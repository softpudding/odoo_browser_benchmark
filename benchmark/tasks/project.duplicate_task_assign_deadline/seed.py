"""Seed a project task for the duplicate-task-assign-deadline task.

Category 2 (MEDIUM): use the Action menu on a task form to duplicate one task,
then adjust a few fields on the duplicated record without touching the
original or the distractor task.
"""

PROJECT_NAME = "Operations Knowledge Base"
TARGET_TASK = "Draft launch checklist"
COPY_TASK = "Draft launch checklist follow-up"
DISTRACTOR_TASK = "Draft launch checklist mobile"


def _ensure_stage(env, name, sequence):
    stage = env["project.task.type"].search([("name", "=", name)], limit=1)
    if not stage:
        stage = env["project.task.type"].create({
            "name": name,
            "sequence": sequence,
        })
    return stage


def setup(env):
    stage_todo = _ensure_stage(env, "To Do", 1)
    stage_in_progress = _ensure_stage(env, "In Progress", 10)

    project = env["project.project"].search([("name", "=", PROJECT_NAME)], limit=1)
    if not project:
        project = env["project.project"].create({
            "name": PROJECT_NAME,
            "type_ids": [(6, 0, [stage_todo.id, stage_in_progress.id])],
        })
    else:
        project.type_ids = [(6, 0, [stage_todo.id, stage_in_progress.id])]

    env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "in", [TARGET_TASK, COPY_TASK, DISTRACTOR_TASK]),
    ]).unlink()

    env["project.task"].create({
        "name": TARGET_TASK,
        "project_id": project.id,
        "stage_id": stage_todo.id,
        "description": "Review the launch checklist before the support handoff.",
    })
    env["project.task"].create({
        "name": DISTRACTOR_TASK,
        "project_id": project.id,
        "stage_id": stage_todo.id,
        "description": "Keep the mobile notes separate from the main checklist.",
    })
