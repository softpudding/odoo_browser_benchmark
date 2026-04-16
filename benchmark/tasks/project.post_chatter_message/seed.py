"""Seed a project with a task in In Progress stage for the chatter message task.

Category 5: Deep UI interaction (EASY).
The task requires opening a task and posting a regular message in the chatter
using "Send message". This is the simplest chatter interaction — no distinction
between "Log note" and "Send message" is needed.
"""


def setup(env):
    # --- Cleanup prior runs ---
    old_project = env["project.project"].search([("name", "=", "Omega Platform Launch")])
    for proj in old_project:
        proj.task_ids.unlink()
    old_project.unlink()

    # --- Create stages if needed ---
    in_progress_stage = env["project.task.type"].search(
        [("name", "=", "In Progress")], limit=1
    )
    if not in_progress_stage:
        in_progress_stage = env["project.task.type"].create({
            "name": "In Progress",
            "sequence": 10,
        })

    # --- Create project ---
    project = env["project.project"].create({
        "name": "Omega Platform Launch",
        "privacy_visibility": "followers",
        "type_ids": [
            (4, in_progress_stage.id),
        ],
    })

    # --- Create the target task in In Progress ---
    env["project.task"].create({
        "name": "Write API integration spec",
        "project_id": project.id,
        "stage_id": in_progress_stage.id,
        "description": "Document the REST API endpoints needed for the integration layer.",
    })
