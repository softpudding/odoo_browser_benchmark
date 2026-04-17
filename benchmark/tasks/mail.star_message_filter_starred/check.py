"""Postcondition checks for mail.star_message_filter_starred."""

TARGET_MARKER = "Finance close blocker — action required for Q2 cutoff"
DISTRACTOR_MARKERS = [
    "Office WiFi upgrade – FYI",
    "Welcome lunch sign-up",
]


def check(env):
    failures = []

    admin = env.ref("base.user_admin")

    target = env["mail.message"].search([("body", "ilike", TARGET_MARKER)], limit=1)
    if not target:
        return [f"Target message with '{TARGET_MARKER}' not found — seed failed"]

    if admin.partner_id not in target.starred_partner_ids:
        failures.append(
            f"Target message with '{TARGET_MARKER}' is not starred by admin"
        )

    # Make sure the distractors were not starred.
    for marker in DISTRACTOR_MARKERS:
        m = env["mail.message"].search([("body", "ilike", marker)], limit=1)
        if m and admin.partner_id in m.starred_partner_ids:
            failures.append(
                f"Distractor message with '{marker}' was starred — only the "
                f"target message should be starred"
            )

    return failures
