"""Clean up artifacts from previous runs.

Wipes the calendar.event named 'Q2 Planning Session' plus any
ir.attachment rows linked to it, so the seed can re-run deterministically.
"""

EVENT_NAME = "Q2 Planning Session"


def cleanup(env):
    events = env["calendar.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    if events:
        attachments = env["ir.attachment"].search([
            ("res_model", "=", "calendar.event"),
            ("res_id", "in", events.ids),
        ])
        if attachments:
            attachments.unlink()
        events.unlink()
