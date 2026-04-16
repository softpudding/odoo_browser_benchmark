"""Seed data for project.duplicate_task_assign_deadline."""

PROJECT_NAME = "Launch Enablement Board"
TARGET_TASK = "Prepare webinar outline"
COPY_TASK = "Prepare webinar outline - APAC"
DISTRACTOR_TASK = "Prepare sales deck"


def _ensure_stage(env, name, sequence):
    stage = env["project.task.type"].search([("name", "=", name)], limit=1)
    if not stage:
        stage = env["project.task.type"].create({"name": name, "sequence": sequence})
    return stage


def setup(env):
    todo = _ensure_stage(env, "To Do", 1)
    progress = _ensure_stage(env, "In Progress", 10)

    project = env["project.project"].search([("name", "=", PROJECT_NAME)], limit=1)
    if project:
        env["project.task"].with_context(active_test=False).search([
            ("project_id", "=", project.id),
            ("name", "in", [TARGET_TASK, COPY_TASK, DISTRACTOR_TASK]),
        ]).unlink()
        project.write({"type_ids": [(6, 0, [todo.id, progress.id])]})
    else:
        project = env["project.project"].create({
            "name": PROJECT_NAME,
            "type_ids": [(6, 0, [todo.id, progress.id])],
        })

    env["project.task"].create({
        "name": TARGET_TASK,
        "project_id": project.id,
        "stage_id": todo.id,
        "description": "Reuse the webinar outline for regional launch work.",
    })
    env["project.task"].create({
        "name": DISTRACTOR_TASK,
        "project_id": project.id,
        "stage_id": todo.id,
        "description": "Keep sales enablement tasks separate from webinar planning.",
    })
