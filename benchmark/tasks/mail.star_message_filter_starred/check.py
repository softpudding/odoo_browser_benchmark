"""Postcondition checks for mail.star_message_filter_starred."""

TARGET_SUBJECT = "Finance close blocker — action required for Q2 cutoff"
DISTRACTOR_SUBJECTS = [
    "Office WiFi upgrade – FYI",
    "Welcome lunch sign-up",
]


def check(env):
    failures = []

    admin = env.ref("base.user_admin")

    target = env["mail.message"].search([("subject", "=", TARGET_SUBJECT)], limit=1)
    if not target:
        return [f"Target message '{TARGET_SUBJECT}' not found — seed failed"]

    if admin.partner_id not in target.starred_partner_ids:
        failures.append(
            f"Target message '{TARGET_SUBJECT}' is not starred by admin"
        )

    # Make sure the distractors were not starred.
    for subj in DISTRACTOR_SUBJECTS:
        m = env["mail.message"].search([("subject", "=", subj)], limit=1)
        if m and admin.partner_id in m.starred_partner_ids:
            failures.append(
                f"Distractor message '{subj}' was starred — only the target "
                f"message should be starred"
            )

    return failures
