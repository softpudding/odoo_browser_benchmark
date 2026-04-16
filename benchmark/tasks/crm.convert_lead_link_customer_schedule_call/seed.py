"""Seed a medium CRM lead-conversion workflow.

Category 2 (MEDIUM): the agent must find the correct lead, use the conversion
wizard to link it to an existing customer, then finish the opportunity setup
without leaving CRM.
"""

TARGET_NAME = "Summit Ridge Support Rollout"
DISTRACTOR_NAME = "Summit Ridge Support Review"
TARGET_CUSTOMER = "Summit Ridge Manufacturing"
DISTRACTOR_CUSTOMER = "Summit Ridge Materials"
TARGET_ACTIVITY = "Review support rollout scope"


def _cleanup(env):
    env["mail.activity"].search([("summary", "=", TARGET_ACTIVITY)]).unlink()
    env["crm.lead"].search([
        ("name", "in", [TARGET_NAME, DISTRACTOR_NAME]),
    ]).unlink()


def _ensure_partner(env, name, email):
    partner = env["res.partner"].search([("name", "=", name)], limit=1)
    if partner:
        partner.write({"email": email, "customer_rank": 1})
        return partner
    return env["res.partner"].create({
        "name": name,
        "email": email,
        "customer_rank": 1,
    })


def setup(env):
    _cleanup(env)

    admin = env.ref("base.user_admin")
    sales_team = env["crm.team"].search([("name", "=", "Sales")], limit=1)
    lead_group = env.ref("crm.group_use_lead", raise_if_not_found=False)
    if lead_group:
        lead_group.write({"user_ids": [(4, admin.id)]})
    if sales_team:
        sales_team.write({"use_leads": True, "use_opportunities": True})

    _ensure_partner(env, TARGET_CUSTOMER, "ops@summitridge.example.com")
    _ensure_partner(env, DISTRACTOR_CUSTOMER, "materials@summitridge.example.com")

    common_vals = {
        "type": "lead",
        "team_id": sales_team.id if sales_team else False,
        "user_id": admin.id,
    }

    env["crm.lead"].create({
        **common_vals,
        "name": TARGET_NAME,
        "partner_name": "Summit Ridge",
        "contact_name": "Maya Torres",
        "email_from": "maya.torres@summitridge.example.com",
        "phone": "+1 555 0142",
        "description": "Target lead that should be converted and scheduled.",
    })
    env["crm.lead"].create({
        **common_vals,
        "name": DISTRACTOR_NAME,
        "partner_name": "Summit Ridge",
        "contact_name": "Evan Price",
        "email_from": "evan.price@summitridge.example.com",
        "phone": "+1 555 0198",
        "description": "Distractor lead that must remain untouched.",
    })
