"""Seed duplicate CRM opportunities for a merge workflow task."""


TARGET_EMAIL = "renewal@northwind.example.com"
DISTRACTOR_EMAIL = "ops@westwind.example.com"
TARGET_ACTIVITY = "Northwind duplicate cleanup"


def setup(env):
    sales_team = env["crm.team"].search([("name", "=", "Sales")], limit=1)
    admin = env["res.users"].search([("login", "=", "admin")], limit=1)

    env["mail.activity"].search([("summary", "=", TARGET_ACTIVITY)]).unlink()
    env["crm.lead"].search([("email_from", "in", [TARGET_EMAIL, DISTRACTOR_EMAIL])]).unlink()

    common = {
        "type": "opportunity",
        "team_id": sales_team.id if sales_team else False,
        "user_id": admin.id if admin else False,
        "stage_id": env["crm.stage"].search([("name", "=", "New")], limit=1).id,
    }

    env["crm.lead"].create({
        **common,
        "name": "Northwind Advisory Renewal",
        "partner_name": "Northwind Advisory",
        "contact_name": "Avery Stone",
        "email_from": TARGET_EMAIL,
        "phone": "+1 555 0110",
        "expected_revenue": 9000.0,
        "description": "Primary duplicate opportunity.",
    })
    env["crm.lead"].create({
        **common,
        "name": "Northwind Advisory Renewal Follow-up",
        "partner_name": "Northwind Advisory",
        "contact_name": "Avery Stone",
        "email_from": TARGET_EMAIL,
        "phone": "+1 555 0110",
        "expected_revenue": 12000.0,
        "description": "Secondary duplicate opportunity.",
    })
    env["crm.lead"].create({
        **common,
        "name": "Westwind Logistics Renewal",
        "partner_name": "Westwind Logistics",
        "contact_name": "Morgan Tate",
        "email_from": DISTRACTOR_EMAIL,
        "phone": "+1 555 0199",
        "expected_revenue": 7000.0,
        "description": "Distractor opportunity.",
    })
