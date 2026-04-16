"""Seed a project with three tasks for the archive-with-log-note task.

Category 2 (MEDIUM): The agent must find the right task, post an
internal log note with exact text, then archive the task via the
Action menu. Capability tested: Archive action + log-note chatter
interaction without touching sibling tasks.
"""


def setup(env):
    # --- Cleanup prior runs ---
    project = env["project.project"].search(
        [("name", "=", "Nexus Platform Launch")], limit=1
    )
    if project:
        tasks = env["project.task"].with_context(active_test=False).search([
            ("project_id", "=", project.id),
        ])
        # Clear prior notes first
        for task in tasks:
            env["mail.message"].search([
                ("res_model", "=", "project.task"),
                ("res_id", "=", task.id),
                ("subtype_id.name", "=", "Note"),
            ]).unlink()
        tasks.unlink()
        project.unlink()

    # --- Create fresh project ---
    project = env["project.project"].create({
        "name": "Nexus Platform Launch",
    })

    # --- Create three tasks, middle one is the target ---
    for title in [
        "Kickoff rollout playbook",
        "Retire beta build",
        "Finalize training outline",
    ]:
        env["project.task"].create({
            "name": title,
            "project_id": project.id,
            "active": True,
        })
