"""Postcondition checks for project.complete_task_log_note.

Validates that:
1. The target task moved to the Done stage
2. An internal log note (not a regular message) with exact text was posted
"""

EXPECTED_NOTE = "Spec completed and reviewed by the backend team. Ready for handoff."


def check(env):
    failures = []

    # Find the project
    project = env["project.project"].search(
        [("name", "=", "Omega Platform Launch")], limit=1
    )
    if not project:
        return ["Project 'Omega Platform Launch' not found"]

    # Find the target task
    task = env["project.task"].search([
        ("name", "=", "Write API integration spec"),
        ("project_id", "=", project.id),
    ], limit=1)
    if not task:
        return ["Task 'Write API integration spec' not found in project"]

    # Check task is in Done stage
    if not task.stage_id:
        failures.append("Task has no stage assigned")
    else:
        # The stage should be named "Done" or have fold=True (closed stage)
        stage = task.stage_id
        if stage.name != "Done" and not stage.fold:
            failures.append(
                f"Task stage is '{stage.name}' (fold={stage.fold}), expected 'Done'"
            )

    # Check for internal log note with exact text
    # Internal notes have subtype 'mail.mt_note' or message_type='comment' + is_internal=True
    note_subtype = env.ref("mail.mt_note", raise_if_not_found=False)
    messages = env["mail.message"].search([
        ("model", "=", "project.task"),
        ("res_id", "=", task.id),
        ("message_type", "=", "comment"),
    ])

    # Look for a message that is internal (log note) with the expected text
    found_note = False
    for msg in messages:
        is_internal = msg.subtype_id == note_subtype if note_subtype else msg.is_internal
        if is_internal:
            # Strip HTML tags for comparison
            body_text = msg.body or ""
            # Simple HTML strip: remove tags
            import re
            plain = re.sub(r"<[^>]+>", "", body_text).strip()
            # Normalize whitespace
            plain = " ".join(plain.split())
            if EXPECTED_NOTE in plain:
                found_note = True
                break

    if not found_note:
        # Check if a regular (non-internal) message was posted instead
        regular_msgs = [
            m for m in messages
            if not (m.subtype_id == note_subtype if note_subtype else m.is_internal)
        ]
        if regular_msgs:
            failures.append(
                "A regular 'Send message' was used instead of 'Log note' — "
                "the message must be an internal note"
            )
        else:
            failures.append(
                f"No internal log note found. Expected text: '{EXPECTED_NOTE}'"
            )

    # Verify distractor tasks were not modified
    distractor_names = [
        "Set up CI/CD pipeline",
        "Define data model schema",
        "Conduct security audit",
    ]
    done_stage = env["project.task.type"].search([("name", "=", "Done")], limit=1)
    if done_stage:
        for name in distractor_names:
            t = env["project.task"].search([
                ("name", "=", name),
                ("project_id", "=", project.id),
            ], limit=1)
            if t and t.stage_id == done_stage:
                failures.append(
                    f"Distractor task '{name}' was moved to Done — only the target task should change"
                )

    return failures
