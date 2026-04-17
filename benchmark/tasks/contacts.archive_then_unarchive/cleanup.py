"""Clean up contacts created for this task."""


ACTIVE_NAME = "Wilder Ferris (Bench-Archive-01)"
ARCHIVED_NAME = "Talon Vega (Bench-Archive-02)"


def cleanup(env):
    Partner = env["res.partner"].with_context(active_test=False)
    victims = Partner.search([("name", "in", [ACTIVE_NAME, ARCHIVED_NAME])])
    if victims:
        victims.unlink()
