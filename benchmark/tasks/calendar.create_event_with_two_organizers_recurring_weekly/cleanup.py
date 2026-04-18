"""Clean up artifacts from calendar.create_event_with_two_organizers_recurring_weekly."""


def cleanup(env):
    events = env["calendar.event"].search([("name", "=", "Weekly Standup")])
    recurrences = events.mapped("recurrence_id")
    events.with_context(dont_notify=True).unlink()
    recurrences.unlink()
