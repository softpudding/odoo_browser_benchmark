"""Seed a lead for the lead-email update task."""

LEAD_NAME = "Cobalt Cloud Expansion"
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
        "contact_name": "Cobalt Contact",
        "email_from": "cobalt.sales@cobaltcloud.example.com",
        "phone": "+1 555 0230",
        "team_id": team.id,
        "user_id": admin.id if admin else False,
    })
