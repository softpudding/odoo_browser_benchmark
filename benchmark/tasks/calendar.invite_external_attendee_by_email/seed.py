"""Seed for calendar.invite_external_attendee_by_email.

Easy: agent must create a new calendar event and add an external email
(`vendor.partner@example.com`) as an attendee through the "Create ..."
quick-create option in the m2m_tags autocomplete dropdown. Odoo will then
create a res.partner on-the-fly for that email.

The seed only cleans up artifacts from prior runs — it does NOT pre-create
the event or the external partner.
"""

EVENT_NAME = "Benchmark Strategy Sync"
EXTERNAL_EMAIL = "vendor.partner@example.com"


def setup(env):
    # Cleanup prior runs: delete any event with this name and any partner
    # with the external email so the agent starts from a clean slate.
    env["calendar.event"].search([("name", "=", EVENT_NAME)]).unlink()
    env["res.partner"].search([("email", "=", EXTERNAL_EMAIL)]).unlink()
