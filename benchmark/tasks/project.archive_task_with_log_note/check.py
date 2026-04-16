"""Postcondition checks for project.archive_task_with_log_note.

Validates:
1. Task "Retire beta build" exists but is archived (active=False).
2. An internal log note (subtype 'Note') with the expected body is
   attached to that task.
3. The other two tasks remain active and untouched.
"""


EXPECTED_NOTE = (
    "Superseded by v2 pipeline. Archiving to clear the active backlog."
)


def check(env):
    failures = []

    project = env["project.project"].search(
        [("name", "=", "Nexus Platform Launch")], limit=1
    )
    if not project:
        return ["Project 'Nexus Platform Launch' not found"]

    Task = env["project.task"].with_context(active_test=False)

    target = Task.search([
        ("project_id", "=", project.id),
        ("name", "=", "Retire beta build"),
    ], limit=1)
    if not target:
        failures.append("Task 'Retire beta build' not found")
    else:
        if target.active:
            failures.append(
                "Task 'Retire beta build' is still active, expected archived"
            )
        notes = env["mail.message"].search([
            ("res_model", "=", "project.task"),
            ("res_id", "=", target.id),
            ("subtype_id.name", "=", "Note"),
        ])
        found = any(
            n.body and EXPECTED_NOTE in (n.body or "")
            for n in notes
        )
        if not found:
            bodies = [n.body[:120] for n in notes if n.body]
            failures.append(
                f"Internal log note '{EXPECTED_NOTE}' not found. "
                f"Notes on task: {bodies}"
            )

    # Siblings must still be active
    for title in ("Kickoff rollout playbook", "Finalize training outline"):
        sibling = Task.search([
            ("project_id", "=", project.id),
            ("name", "=", title),
        ], limit=1)
        if not sibling:
            failures.append(f"Sibling task '{title}' is missing")
        elif not sibling.active:
            failures.append(
                f"Sibling task '{title}' was archived; expected still active"
            )

    return failures
