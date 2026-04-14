"""Seed a CRM-to-sales handoff workflow with a modal conversion step."""


TARGET_EMAIL = "ops-east@northwind.example.com"
WEST_EMAIL = "ops-west@northwind.example.com"
TARGET_PARTNER = "Northwind Advisory East"
WEST_PARTNER = "Northwind Advisory West"
TARGET_TAG = "Executive Review"
TARGET_ACTIVITY = "Northwind discovery handoff"
TARGET_REF = "CRM-HANDOFF-24"


def setup(env):
    admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    sales_team = env["crm.team"].search([("name", "=", "Sales")], limit=1)
    lead_group = env.ref("crm.group_use_lead", raise_if_not_found=False)

    if admin and lead_group:
        lead_group.write({"user_ids": [(4, admin.id)]})
    if sales_team:
        sales_team.write({
            "use_leads": True,
            "use_opportunities": True,
        })

    env["sale.order"].search([("client_order_ref", "=", TARGET_REF)]).unlink()
    env["mail.activity"].search([("summary", "=", TARGET_ACTIVITY)]).unlink()
    env["crm.lead"].search([("email_from", "in", [TARGET_EMAIL, WEST_EMAIL])]).unlink()

    east = env["res.partner"].search([("name", "=", TARGET_PARTNER)], limit=1)
    if east:
        east.write({"email": "east@northwind.example.com"})
    else:
        east = env["res.partner"].create({
            "name": TARGET_PARTNER,
            "email": "east@northwind.example.com",
        })

    west = env["res.partner"].search([("name", "=", WEST_PARTNER)], limit=1)
    if west:
        west.write({"email": "west@northwind.example.com"})
    else:
        west = env["res.partner"].create({
            "name": WEST_PARTNER,
            "email": "west@northwind.example.com",
        })

    tag = env["crm.tag"].search([("name", "=", TARGET_TAG)], limit=1)
    if not tag:
        env["crm.tag"].create({"name": TARGET_TAG})

    common_vals = {
        "type": "lead",
        "team_id": sales_team.id if sales_team else False,
        "user_id": admin.id if admin else False,
    }

    env["crm.lead"].create({
        **common_vals,
        "name": "Northwind Advisory Platform Rollout",
        "partner_name": "Northwind Advisory",
        "contact_name": "Avery Stone",
        "email_from": TARGET_EMAIL,
        "phone": "+1 555 0102",
        "description": "Target lead for the approval workflow handoff.",
    })

    env["crm.lead"].create({
        **common_vals,
        "name": "Northwind Advisory Renewal Follow-up",
        "partner_name": "Northwind Advisory",
        "contact_name": "Morgan Tate",
        "email_from": WEST_EMAIL,
        "phone": "+1 555 0177",
        "description": "Distractor lead that must stay untouched.",
    })
