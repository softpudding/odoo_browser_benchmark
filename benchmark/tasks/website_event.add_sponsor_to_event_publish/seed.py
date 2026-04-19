"""Seed for website_event.add_sponsor_to_event_publish.

Installs website_event + website_event_exhibitor (both outside the base
snapshot) so the Sponsors smart button + event.sponsor model are available.
Seeds:
- unpublished event `Bench Conf 2026`
- partner `Bench Sponsor Inc`
- ensures sponsor level `Silver` exists (installed by default data in
  website_event_exhibitor, but we defensively find-or-create)

Agent opens the event, clicks the Sponsors smart button, creates a sponsor
pointing at Bench Sponsor Inc with level Silver, saves, and publishes the
event via the website systray toggle.
"""


EVENT_NAME = "Bench Conf 2026"
PARTNER_NAME = "Bench Sponsor Inc"
SPONSOR_LEVEL = "Silver"


def _ensure_module(env, name):
    mod = env["ir.module.module"].search([("name", "=", name)], limit=1)
    if not mod:
        return
    if mod.state != "installed":
        mod.button_immediate_install()


def setup(env):
    # website_event_exhibitor transitively depends on website_event; both
    # are absent from the benchmark base snapshot.
    _ensure_module(env, "website_event")
    _ensure_module(env, "website_event_exhibitor")

    # ----- Cleanup prior runs (child-first) -----
    prior_events = env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    # Delete any sponsors attached to prior events with this name first.
    env["event.sponsor"].with_context(active_test=False).search([
        ("event_id", "in", prior_events.ids),
    ]).sudo().unlink()
    prior_events.mapped("registration_ids").sudo().unlink()
    prior_events.sudo().unlink()

    # Leave the partner alive across runs if possible (so we don't churn
    # the res.partner id unnecessarily), but drop stray sponsors that
    # reference the seeded partner from past runs on other (deleted)
    # events to keep the DB clean.
    prior_partners = env["res.partner"].with_context(active_test=False).search([
        ("name", "=", PARTNER_NAME),
    ])
    env["event.sponsor"].with_context(active_test=False).search([
        ("partner_id", "in", prior_partners.ids),
    ]).sudo().unlink()

    # ----- Ensure the seeded partner exists -----
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": PARTNER_NAME,
            "email": "sponsor@example.com",
            "is_company": True,
        })

    # ----- Ensure the Silver sponsor level exists (default data) -----
    level = env["event.sponsor.type"].search([("name", "=", SPONSOR_LEVEL)], limit=1)
    if not level:
        env["event.sponsor.type"].create({
            "name": SPONSOR_LEVEL,
            "display_ribbon_style": "Silver",
            "sequence": 2,
        })

    # ----- Create the target event, unpublished -----
    values = {
        "name": EVENT_NAME,
        "date_begin": "2026-09-10 09:00:00",
        "date_end": "2026-09-11 17:00:00",
    }
    if "is_published" in env["event.event"]._fields:
        values["is_published"] = False
    if "website_published" in env["event.event"]._fields:
        values["website_published"] = False

    env["event.event"].create(values)
