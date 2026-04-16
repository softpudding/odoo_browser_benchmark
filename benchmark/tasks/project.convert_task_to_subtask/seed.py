"""Seed project tasks for the convert-task-to-subtask task.

Category 2 (MEDIUM): the agent must open the correct standalone project task,
use the built-in Convert to Task/Sub-Task action, select the right parent in
the dialog, and then update the deadline without touching the parent task.
"""

PROJECT_NAME = "Atlas Support Rollout"
TASK_NAME = "Vendor readiness checklist"
PARENT_TASK = "Launch coordination"
DISTRACTOR_TASK = "Archived coordination notes"
TASK_DESCRIPTION = "Track the remaining supplier confirmations before launch."


def _ensure_stage(env, project, name, sequence):
    stage = env["project.task.type"].search([
        ("name", "=", name),
        ("project_ids", "in", [project.id]),
    ], limit=1)
    if stage:
        return stage

    global_stage = env["project.task.type"].search([("name", "=", name)], limit=1)
    if global_stage:
        global_stage.write({"project_ids": [(4, project.id)]})
        return global_stage

    return env["project.task.type"].create({
        "name": name,
        "sequence": sequence,
        "project_ids": [(4, project.id)],
    })

def setup(env):
    project = env["project.project"].search([("name", "=", PROJECT_NAME)], limit=1)
    if not project:
        project = env["project.project"].create({"name": PROJECT_NAME})

    todo = _ensure_stage(env, project, "To Do", 10)
    in_progress = _ensure_stage(env, project, "In Progress", 20)
    _ensure_stage(env, project, "Done", 30)

    existing = env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "in", [TASK_NAME, PARENT_TASK, DISTRACTOR_TASK]),
    ])
    existing.unlink()

    env["project.task"].create({
        "name": PARENT_TASK,
        "project_id": project.id,
        "stage_id": in_progress.id,
        "description": "Coordinate the final launch workstream.",
    })

    env["project.task"].create({
        "name": TASK_NAME,
        "project_id": project.id,
        "stage_id": todo.id,
        "description": TASK_DESCRIPTION,
    })

    env["project.task"].create({
        "name": DISTRACTOR_TASK,
        "project_id": project.id,
        "stage_id": in_progress.id,
        "description": "Archive the prior launch coordination notes.",
        "date_deadline": "2026-05-10",
    })
