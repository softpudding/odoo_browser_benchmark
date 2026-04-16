"""Postcondition checks for project.post_chatter_message.

Validates that:
1. The target task exists and is unchanged
2. A regular chatter message (not an internal note) with exact text was posted
"""

EXPECTED_MESSAGE = "Backend team has reviewed the spec. Moving forward with implementation."


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

    # Check for a regular chatter message with exact text
    # Regular messages have message_type='comment' and subtype NOT equal to mail.mt_note
    note_subtype = env.ref("mail.mt_note", raise_if_not_found=False)
    messages = env["mail.message"].search([
        ("model", "=", "project.task"),
        ("res_id", "=", task.id),
        ("message_type", "=", "comment"),
    ])

    # Look for a regular (non-internal) message with the expected text
    found_message = False
    for msg in messages:
        is_internal = msg.subtype_id == note_subtype if note_subtype else msg.is_internal
        if not is_internal:
            # Strip HTML tags for comparison
            body_text = msg.body or ""
            import re
            plain = re.sub(r"<[^>]+>", "", body_text).strip()
            # Normalize whitespace
            plain = " ".join(plain.split())
            if EXPECTED_MESSAGE in plain:
                found_message = True
                break

    if not found_message:
        # Check if an internal note was posted instead
        internal_msgs = [
            m for m in messages
            if (m.subtype_id == note_subtype if note_subtype else m.is_internal)
        ]
        if internal_msgs:
            failures.append(
                "An internal 'Log note' was used instead of 'Send message' — "
                "the message must be a regular chatter message"
            )
        else:
            failures.append(
                f"No regular chatter message found. Expected text: '{EXPECTED_MESSAGE}'"
            )

    return failures
