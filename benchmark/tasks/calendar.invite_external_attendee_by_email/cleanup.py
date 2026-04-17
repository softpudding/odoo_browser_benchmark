"""Clean up artifacts from previous runs of calendar.invite_external_attendee_by_email."""


EVENT_NAME = "Benchmark Strategy Sync"
EXTERNAL_EMAIL = "vendor.partner@example.com"


def cleanup(env):
    env["calendar.event"].search([("name", "=", EVENT_NAME)]).unlink()
    env["res.partner"].search([("email", "=", EXTERNAL_EMAIL)]).unlink()
