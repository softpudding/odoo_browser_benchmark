"""Seed a project task for the deadline-setting task.

Category: deep_ui_interaction (EASY).
Starting state: Project "Omega Platform Launch" with task "Design Landing Page Mockup"
with deadline set to April 30, 2026. The agent must change it to May 20, 2026.
"""


def setup(env):
    # --- Cleanup prior runs ---
    env["project.task"].search([("name", "=", "Design Landing Page Mockup")]).unlink()

    # --- Ensure project exists ---
    project = env["project.project"].search([("name", "=", "Omega Platform Launch")], limit=1)
    if not project:
        project = env["project.project"].create({
            "name": "Omega Platform Launch",
        })

    # --- Ensure a task stage exists ---
    stage = env["project.task.type"].search([("name", "=", "In Progress")], limit=1)
    if not stage:
        stage = env["project.task.type"].create({
            "name": "In Progress",
            "sequence": 2,
        })

    # --- Create the target task ---
    admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    env["project.task"].create({
        "name": "Design Landing Page Mockup",
        "project_id": project.id,
        "stage_id": stage.id,
        "date_deadline": "2026-04-30",
        "user_ids": [(6, 0, [admin.id])] if admin else False,
        "description": "Design the landing page mockup for the Omega platform.",
    })