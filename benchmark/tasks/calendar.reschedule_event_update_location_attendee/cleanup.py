"""Clean up artifacts from previous runs."""


def cleanup(env):
    env["calendar.event"].search([
        ("name", "in", ["Warehouse Safety Briefing", "Warehouse Safety Briefing - East"]),
    ]).unlink()
