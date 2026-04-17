"""Seed a lead for the lead-phone update task."""

LEAD_NAME = "Summit Energy Expansion"
TEAM_NAME = "Sales"
USER_LOGIN = "admin"


def setup(env):
    env["crm.lead"].search([("name", "=", LEAD_NAME)]).unlink()

    team = env["crm.team"].search([("name", "=", TEAM_NAME)], limit=1)
    if not team:
        team = env["crm.team"].create({"name": TEAM_NAME})

    admin = env["res.users"].search([("login", "=", USER_LOGIN)], limit=1)

    env["crm.lead"].create({
        "name": LEAD_NAME,
        "type": "lead",
        "partner_name": "Summit Energy",
        "contact_name": "Jordan Lee",
        "email_from": "leads@summit-energy.example.com",
        "phone": "+1 555 0220",
        "team_id": team.id,
        "user_id": admin.id if admin else False,
    })
