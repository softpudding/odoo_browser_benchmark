"""Seed for calendar.create_meeting_invite_attendees_send.

Difficulty: medium (Category: deep_ui_interaction).
The agent must:
  - Create a calendar.event 'Team Sync' on 2026-05-20 10:00-11:00 local.
  - Add two seeded res.partner contacts (Attendee Alpha + Attendee Beta) via
    the partner_ids many2many_tags autocomplete.
  - Save the event.

Seed responsibilities:
  - Wipe any prior 'Team Sync' events (and their invitation.ics attachments).
  - Ensure two res.partner rows 'Attendee Alpha' (alpha@bench.test) and
    'Attendee Beta' (beta@bench.test) exist so the agent can pick them from
    the Attendees autocomplete.
  - Do NOT pre-create the event; the agent creates it.
"""

EVENT_NAME = "Team Sync"
ATTENDEE_PARTNERS = (
    {"name": "Attendee Alpha", "email": "alpha@bench.test"},
    {"name": "Attendee Beta", "email": "beta@bench.test"},
)


def setup(env):
    # Cleanup any leftover event(s) from previous runs (and their
    # auto-created invitation.ics attachments so cleanup is fully idempotent).
    events = env["calendar.event"].with_context(active_test=False).search([
        ("name", "=", EVENT_NAME),
    ])
    if events:
        attachments = env["ir.attachment"].search([
            ("res_model", "=", "calendar.event"),
            ("res_id", "in", events.ids),
        ])
        if attachments:
            attachments.unlink()
        events.unlink()

    # Ensure the two attendee partners exist. Match by exact name so repeated
    # runs don't accumulate duplicates.
    for spec in ATTENDEE_PARTNERS:
        partner = env["res.partner"].with_context(active_test=False).search(
            [("name", "=", spec["name"])], limit=1,
        )
        if partner:
            if not partner.active:
                partner.active = True
            if (partner.email or "") != spec["email"]:
                partner.email = spec["email"]
            continue
        env["res.partner"].create({
            "name": spec["name"],
            "email": spec["email"],
        })
