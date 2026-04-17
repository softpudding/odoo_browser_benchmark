"""Postcondition checks for mail.mark_message_as_todo_and_resolve."""

CHANNEL_NAME = "benchmarks-ops"
EXPECTED_REPLY_SNIPPET = "rescheduling to 5 AM on weekdays"


def check(env):
    failures = []

    admin = env.ref("base.user_admin")

    channel = env["discuss.channel"].search([
        ("name", "=", CHANNEL_NAME),
    ], limit=1)
    if not channel:
        return [f"Channel '#{CHANNEL_NAME}' not found"]

    # Find the anchor message (the original question).
    anchor_candidates = env["mail.message"].search([
        ("model", "=", "discuss.channel"),
        ("res_id", "=", channel.id),
    ])
    anchor = None
    for m in anchor_candidates:
        if "3 AM warehouse sync" in (m.body or ""):
            anchor = m
            break
    if not anchor:
        return [
            "Anchor message about the '3 AM warehouse sync' was not "
            "found — seed may have failed"
        ]

    # Look for admin's reply whose parent_id is the anchor.
    replies = env["mail.message"].search([
        ("model", "=", "discuss.channel"),
        ("res_id", "=", channel.id),
        ("author_id", "=", admin.partner_id.id),
        ("parent_id", "=", anchor.id),
    ])
    if not replies:
        return [
            "No in-thread reply from admin found — the message must have "
            "parent_id pointing at the anchor (use Reply in Thread)"
        ]

    if not any(EXPECTED_REPLY_SNIPPET in (m.body or "") for m in replies):
        failures.append(
            f"Reply does not contain required snippet "
            f"'{EXPECTED_REPLY_SNIPPET}'"
        )

    return failures
