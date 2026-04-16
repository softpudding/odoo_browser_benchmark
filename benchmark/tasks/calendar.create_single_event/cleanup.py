"""Clean up artifacts from previous runs."""


def cleanup(env):
    events = env["calendar.event"].search([("name", "=", "Q2 Strategy Review")])
    events.unlink()
