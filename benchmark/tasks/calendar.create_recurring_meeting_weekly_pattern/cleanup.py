"""Clean up artifacts from calendar.create_recurring_meeting_weekly_pattern."""


EVENT_NAME = "Bench Weekly Standup"


def cleanup(env):
    events = env["calendar.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    if events:
        recurrences = events.mapped("recurrence_id")
        attachments = env["ir.attachment"].search([
            ("res_model", "=", "calendar.event"),
            ("res_id", "in", events.ids),
        ])
        if attachments:
            attachments.unlink()
        events.with_context(dont_notify=True).unlink()
        if recurrences:
            recurrences.unlink()
