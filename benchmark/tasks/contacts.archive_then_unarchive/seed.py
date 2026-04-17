"""Seed two contacts for contacts.archive_then_unarchive: one active to archive, one archived to unarchive."""


ACTIVE_NAME = "Wilder Ferris (Bench-Archive-01)"
ARCHIVED_NAME = "Talon Vega (Bench-Archive-02)"


def setup(env):
    Partner = env["res.partner"].with_context(active_test=False)
    existing = Partner.search([("name", "in", [ACTIVE_NAME, ARCHIVED_NAME])])
    if existing:
        existing.unlink()

    Partner.create({
        "name": ACTIVE_NAME,
        "email": "wilder@bench-archive.test",
        "phone": "+1 555 0100",
        "is_company": False,
        "active": True,
    })
    Partner.create({
        "name": ARCHIVED_NAME,
        "email": "talon@bench-archive.test",
        "phone": "+1 555 0101",
        "is_company": False,
        "active": False,
    })
