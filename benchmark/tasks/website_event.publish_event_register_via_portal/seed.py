"""Seed for website_event.publish_event_register_via_portal.

Category: closed-loop cross-module (back-office <-> public portal).

Installs `website_event` on demand (not in the base snapshot), then
creates a single unpublished event `Bench Public Day` with NO tickets
configured (so the default "Registration" generic ticket is used on the
public portal modal).

The agent must publish the event in the back-office and then complete
the public registration form on /event.

Cleanup is child-first (registrations -> events) and is performed
first so the task is idempotent across re-runs.
"""

EVENT_NAME = "Bench Public Day"
ATTENDEE_NAME = "Priya Patel"
ATTENDEE_EMAIL = "priya.patel@example.com"


def _ensure_module(env, name):
    mod = env["ir.module.module"].search([("name", "=", name)], limit=1)
    if not mod:
        return
    if mod.state != "installed":
        mod.button_immediate_install()


def setup(env):
    # Make sure website_event is installed (not in the base snapshot).
    _ensure_module(env, "website_event")

    # ----- Cleanup prior runs (child-first) -----
    env["event.registration"].with_context(active_test=False).search([
        "|", "|",
        ("name", "=", ATTENDEE_NAME),
        ("email", "=", ATTENDEE_EMAIL),
        ("event_id.name", "=", EVENT_NAME),
    ]).sudo().unlink()

    env["event.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ]).sudo().unlink()

    # ----- Create the target event, unpublished -----
    values = {
        "name": EVENT_NAME,
        "date_begin": "2026-07-10 09:00:00",
        "date_end": "2026-07-10 17:00:00",
    }
    # Defensively keep it unpublished.
    if "is_published" in env["event.event"]._fields:
        values["is_published"] = False
    if "website_published" in env["event.event"]._fields:
        values["website_published"] = False

    env["event.event"].create(values)
