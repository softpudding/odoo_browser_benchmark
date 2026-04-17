"""Seed for calendar.create_private_meeting_with_video_link."""

EVENT_NAME = "Private Vendor Sync"


def setup(env):
    env["calendar.event"].search([("name", "=", EVENT_NAME)]).unlink()
    marc = env["res.users"].search([("name", "=", "Marc Demo")], limit=1)
    if not marc:
        marc_partner = env["res.partner"].search([("name", "=", "Marc Demo")], limit=1)
        if not marc_partner:
            marc_partner = env["res.partner"].create({
                "name": "Marc Demo",
                "email": "marc.demo@company.com",
            })
        env["res.users"].create({
            "name": "Marc Demo",
            "login": "marc.demo",
            "partner_id": marc_partner.id,
        })
