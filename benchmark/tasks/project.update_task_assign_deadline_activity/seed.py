"""Seed a project task for the update-task-assign-deadline-activity task.

Category 2 (MEDIUM): Edit an existing task, move its stage, assign a user,
set a deadline, and schedule an activity from the chatter.
"""

PROJECT_NAME = "Customer Portal Refresh"
TARGET_TASK = "Revise FAQ copy"
DISTRACTOR_TASK = "Revise API docs"
ACTIVITY_SUMMARY = "Review FAQ revisions"


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
    env["mail.activity"].search([("summary", "=", ACTIVITY_SUMMARY)]).unlink()

    project = env["project.project"].search([("name", "=", PROJECT_NAME)], limit=1)
    if not project:
        project = env["project.project"].create({"name": PROJECT_NAME})

    user = env["res.users"].search([("name", "=", "Mitchell Admin")], limit=1)
    if not user:
        user = env["res.users"].create({
            "name": "Mitchell Admin",
            "login": "mitchell.admin",
            "email": "mitchell.admin@example.com",
        })

    todo = _ensure_stage(env, project, "To Do", 10)
    in_progress = _ensure_stage(env, project, "In Progress", 20)
    _ensure_stage(env, project, "Done", 30)

    env["project.task"].search([
        ("project_id", "=", project.id),
        ("name", "in", [TARGET_TASK, DISTRACTOR_TASK]),
    ]).unlink()

    env["project.task"].create({
        "name": TARGET_TASK,
        "project_id": project.id,
        "stage_id": todo.id,
    })
    env["project.task"].create({
        "name": DISTRACTOR_TASK,
        "project_id": project.id,
        "stage_id": todo.id,
    })
