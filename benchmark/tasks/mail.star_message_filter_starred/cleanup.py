"""Cleanup for mail.star_message_filter_starred."""

SUBJECTS = [
    "Finance close blocker — action required for Q2 cutoff",
    "Office WiFi upgrade – FYI",
    "Welcome lunch sign-up",
]


def cleanup(env):
    env["mail.message"].search([("subject", "in", SUBJECTS)]).unlink()
