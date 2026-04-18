"""Seed for crm.assign_team_change_salesperson_log_activity.

Medium: two Many2one swaps (Sales Team + Salesperson) followed by an activity
scheduling wizard (activity type + date + summary). The two Many2one fields
are in different regions of the form and can trip browser agents that only
find the salesperson dropdown (more prominent in the chatter sidebar).
"""

OPP_NAME = "Bench Big Deal"
PARTNER_NAME = "Bench Industries"
PARTNER_EMAIL = "deals@benchindustries.example"
DIRECT_SALES_TEAM = "Direct Sales"
CHANNEL_TEAM = "Channel"
SARA_LOGIN = "sara.sales"
SARA_NAME = "Sara Sales"


def setup(env):
    admin = env.ref("base.user_admin")
    # Normalise admin display name for the prompt to be unambiguous.
    if admin.name != "Mitchell Admin":
        admin.name = "Mitchell Admin"
        admin.partner_id.name = "Mitchell Admin"

    # --- Cleanup prior runs ---
    old_leads = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", OPP_NAME),
    ])
    for lead in old_leads:
        acts = env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "=", lead.id),
        ])
        acts.unlink()
    old_leads.unlink()

    # --- Ensure the two sales teams exist ---
    direct = env["crm.team"].with_context(active_test=False).search([
        ("name", "=", DIRECT_SALES_TEAM),
    ], limit=1)
    if not direct:
        direct = env["crm.team"].create({
            "name": DIRECT_SALES_TEAM,
            "sequence": 1,
            "company_id": False,
        })
    elif not direct.active:
        direct.write({"active": True})

    channel = env["crm.team"].with_context(active_test=False).search([
        ("name", "=", CHANNEL_TEAM),
    ], limit=1)
    if not channel:
        channel = env["crm.team"].create({
            "name": CHANNEL_TEAM,
            "sequence": 2,
            "company_id": False,
        })
    elif not channel.active:
        channel.write({"active": True})

    # --- Ensure Sara Sales salesperson exists ---
    sara = env["res.users"].with_context(active_test=False).search([
        ("login", "=", SARA_LOGIN),
    ], limit=1)
    if not sara:
        sara = env["res.users"].create({
            "name": SARA_NAME,
            "login": SARA_LOGIN,
            "password": SARA_LOGIN,
            "group_ids": [
                (4, env.ref("base.group_user").id),
                (4, env.ref("sales_team.group_sale_salesman").id),
            ],
        })
    else:
        if sara.name != SARA_NAME:
            sara.name = SARA_NAME
        if not sara.active:
            sara.write({"active": True})

    # Make sure Sara is a member of the Channel team so she shows up in the
    # Salesperson autocomplete without needing to pass domain warnings.
    if sara.id not in channel.member_ids.ids:
        channel.write({"member_ids": [(4, sara.id)]})

    # --- Partner ---
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": PARTNER_NAME,
            "is_company": True,
            "email": PARTNER_EMAIL,
        })

    # --- Create the opportunity seeded on Direct Sales + admin ---
    env["crm.lead"].create({
        "name": OPP_NAME,
        "type": "opportunity",
        "partner_id": partner.id,
        "email_from": PARTNER_EMAIL,
        "user_id": admin.id,
        "team_id": direct.id,
        "expected_revenue": 45000.0,
        "probability": 30.0,
        "description": "Hand-off from Direct Sales to Channel.",
    })
