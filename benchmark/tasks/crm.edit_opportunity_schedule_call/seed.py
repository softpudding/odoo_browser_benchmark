"""Seed an opportunity for the edit-opportunity-schedule-call task.

Category 2 (MEDIUM): Edit revenue and probability on an opportunity, then
schedule a Call activity with a specific date and summary via the activity
popover. The activity scheduling widget is a multi-field popover that can
trip up browser agents.
"""

TARGET_NAME = "Beacon Analytics Deal"
TARGET_PARTNER = "Beacon Analytics"
TARGET_EMAIL = "deals@beaconanalytics.com"


def setup(env):
    # --- Cleanup prior runs ---
    old_leads = env["crm.lead"].search([("name", "=", TARGET_NAME)])
    for lead in old_leads:
        # Delete activities first
        activities = env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "=", lead.id),
        ])
        activities.unlink()
        lead.unlink()

    # --- Ensure partner exists ---
    partner = env["res.partner"].search(
        [("name", "=", TARGET_PARTNER)], limit=1
    )
    if not partner:
        partner = env["res.partner"].create({
            "name": TARGET_PARTNER,
            "email": TARGET_EMAIL,
        })

    # --- Ensure CRM stages exist ---
    qualified_stage = env["crm.stage"].search(
        [("name", "=", "Qualified")], limit=1
    )
    if not qualified_stage:
        qualified_stage = env["crm.stage"].create({
            "name": "Qualified",
            "sequence": 2,
        })

    # --- Create the opportunity ---
    sales_team = env["crm.team"].search([("name", "=", "Sales")], limit=1)
    admin = env.ref("base.user_admin")

    env["crm.lead"].create({
        "name": TARGET_NAME,
        "partner_id": partner.id,
        "partner_name": TARGET_PARTNER,
        "email_from": TARGET_EMAIL,
        "type": "opportunity",
        "stage_id": qualified_stage.id,
        "expected_revenue": 50000.0,
        "probability": 40.0,
        "team_id": sales_team.id if sales_team else False,
        "user_id": admin.id,
        "description": "Initial meeting completed. Proposal sent.",
    })
