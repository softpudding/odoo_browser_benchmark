"""Seed a project task for the add-subtask task.

Category: deep_ui_interaction (EASY).
Starting state: Project "Omega Platform Launch" with task "Design Landing Page Mockup"
with no subtasks. The agent must add a subtask "Create Wireframes".
"""

PROJECT_NAME = "Omega Platform Launch"
TASK_NAME = "Design Landing Page Mockup"


def setup(env):
    env["project.task"].search([("name", "=", "Create Wireframes")]).unlink()
    env["project.task"].search([("name", "=", TASK_NAME)]).unlink()

    project = env["project.project"].search([("name", "=", PROJECT_NAME)], limit=1)
    if not project:
        project = env["project.project"].create({
            "name": PROJECT_NAME,
        })

    stage = env["project.task.type"].search([("name", "=", "In Progress")], limit=1)
    if not stage:
        stage = env["project.task.type"].create({
            "name": "In Progress",
            "sequence": 2,
        })

    admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    env["project.task"].create({
        "name": TASK_NAME,
        "project_id": project.id,
        "stage_id": stage.id,
        "date_deadline": "2026-04-30",
        "user_ids": [(6, 0, [admin.id])] if admin else False,
        "description": "Design the landing page mockup for the Omega platform.",
    })