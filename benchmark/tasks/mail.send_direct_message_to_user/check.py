"""Postcondition checks for mail.send_direct_message_to_user."""

EXPECTED_SENTENCE = (
    "The 10:00 product sync is moved to Thursday 14:00"
)


def check(env):
    failures = []

    admin = env.ref("base.user_admin")
    user = env["res.users"].search([("name", "=", "Priya Mehta")], limit=1)
    if not user:
        return ["User 'Priya Mehta' not found — seed failed"]

    # Find the DM channel (chat type) between admin and Priya only.
    chats = env["discuss.channel"].search([
        ("channel_type", "=", "chat"),
    ])
    target = env["discuss.channel"]
    for ch in chats:
        partners = ch.channel_partner_ids
        if (
            admin.partner_id in partners
            and user.partner_id in partners
            and len(partners) == 2
        ):
            target = ch
            break

    if not target:
        return [
            "No direct-message channel found between Administrator and "
            "Priya Mehta"
        ]

    messages = env["mail.message"].search([
        ("model", "=", "discuss.channel"),
        ("res_id", "=", target.id),
        ("author_id", "=", admin.partner_id.id),
    ])
    if not messages:
        return ["DM thread exists but admin has not sent any message"]

    bodies = [(m.body or "") for m in messages]
    if not any(EXPECTED_SENTENCE in (b or "") for b in bodies):
        failures.append(
            f"None of admin's DM messages to Priya contain the required "
            f"sentence: '{EXPECTED_SENTENCE}...'"
        )

    return failures
