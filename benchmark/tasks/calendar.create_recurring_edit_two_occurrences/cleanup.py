"""Clean up artifacts from calendar.create_recurring_edit_two_occurrences."""


def cleanup(env):
    for title in ("Cross-Team Sync", "Cross-Team Review"):
        events = env["calendar.event"].search([("name", "=", title)])
        recurrences = events.mapped("recurrence_id")
        events.with_context(dont_notify=True).unlink()
        recurrences.unlink()
