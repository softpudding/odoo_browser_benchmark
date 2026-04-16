"""Seed a project with a task in In Progress stage for the chatter log-note task.

Category 5: Deep UI interaction.
The task requires two actions: moving a task to Done stage, then posting
an internal log note (NOT a regular message) in the chatter. Browser-use
typically confuses "Log note" with "Send message" — they look similar but
have different semantics. Internal notes have a yellow background and are
not sent to external recipients. The agent must click "Log note", not
"Send message".
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

    done_stage = env["project.task.type"].search(
        [("name", "=", "Done")], limit=1
    )
    if not done_stage:
        done_stage = env["project.task.type"].create({
            "name": "Done",
            "sequence": 40,
            "fold": True,
        })

    # --- Create distractor stages so the project has a full pipeline ---
    for stage_name, seq in [("To Do", 5), ("In Review", 20)]:
        s = env["project.task.type"].search([("name", "=", stage_name)], limit=1)
        if not s:
            env["project.task.type"].create({"name": stage_name, "sequence": seq})

    # --- Create project ---
    project = env["project.project"].create({
        "name": "Omega Platform Launch",
        "privacy_visibility": "followers",
        "type_ids": [
            (4, env["project.task.type"].search([("name", "=", "To Do")], limit=1).id),
            (4, in_progress_stage.id),
            (4, env["project.task.type"].search([("name", "=", "In Review")], limit=1).id),
            (4, done_stage.id),
        ],
    })

    # --- Create the target task in In Progress ---
    env["project.task"].create({
        "name": "Write API integration spec",
        "project_id": project.id,
        "stage_id": in_progress_stage.id,
        "description": "Document the REST API endpoints needed for the integration layer.",
    })

    # --- Create distractor tasks so the project looks realistic ---
    distractor_tasks = [
        ("Set up CI/CD pipeline", "To Do"),
        ("Define data model schema", "In Review"),
        ("Conduct security audit", "To Do"),
    ]
    for task_name, stage_name in distractor_tasks:
        stage = env["project.task.type"].search([("name", "=", stage_name)], limit=1)
        env["project.task"].create({
            "name": task_name,
            "project_id": project.id,
            "stage_id": stage.id,
        })
