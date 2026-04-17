"""Postcondition checks for contacts.archive_then_unarchive."""


ACTIVE_NAME = "Wilder Ferris (Bench-Archive-01)"
ARCHIVED_NAME = "Talon Vega (Bench-Archive-02)"


def check(env):
    failures = []
    Partner = env["res.partner"].with_context(active_test=False)

    to_archive = Partner.search([("name", "=", ACTIVE_NAME)], limit=1)
    if not to_archive:
        failures.append(f"Contact '{ACTIVE_NAME}' not found")
    elif to_archive.active:
        failures.append(f"Contact '{ACTIVE_NAME}' is still active; expected archived")

    to_unarchive = Partner.search([("name", "=", ARCHIVED_NAME)], limit=1)
    if not to_unarchive:
        failures.append(f"Contact '{ARCHIVED_NAME}' not found")
    elif not to_unarchive.active:
        failures.append(f"Contact '{ARCHIVED_NAME}' is still archived; expected active")

    return failures
