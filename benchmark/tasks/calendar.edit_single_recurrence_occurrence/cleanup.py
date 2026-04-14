"""Clean up artifacts from previous runs."""


def cleanup(env):
    events = env["calendar.event"].search([("name", "=", "Ops Standup")])
    recurrences = events.mapped("recurrence_id")
    events.with_context(dont_notify=True).unlink()
    recurrences.unlink()
