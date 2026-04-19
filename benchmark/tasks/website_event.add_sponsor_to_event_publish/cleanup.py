"""Cleanup for website_event.add_sponsor_to_event_publish."""


EVENT_NAME = "Bench Conf 2026"
PARTNER_NAME = "Bench Sponsor Inc"


def cleanup(env):
    # Drop sponsors on target events first.
    events = env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    env["event.sponsor"].with_context(active_test=False).search([
        ("event_id", "in", events.ids),
    ]).sudo().unlink()

    # Drop sponsors that reference the seeded partner anywhere (so the
    # next run starts from a blank slate regardless of which event they
    # were attached to).
    partners = env["res.partner"].with_context(active_test=False).search([
        ("name", "=", PARTNER_NAME),
    ])
    env["event.sponsor"].with_context(active_test=False).search([
        ("partner_id", "in", partners.ids),
    ]).sudo().unlink()

    events.mapped("registration_ids").sudo().unlink()
    events.sudo().unlink()

    # Leave the partner and the Silver sponsor level untouched so subsequent
    # seeds can reuse them (they are treated as shared reference data).
