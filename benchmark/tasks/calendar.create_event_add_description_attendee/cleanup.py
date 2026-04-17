"""Clean up artifacts from previous runs."""


def cleanup(env):
    env["calendar.event"].search([("name", "=", "Vendor Kickoff Briefing")]).unlink()
