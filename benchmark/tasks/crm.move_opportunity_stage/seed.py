"""Seed a single CRM opportunity for the move-opportunity-stage task.

Category 1 (EASY): Move a single clearly identified opportunity from
"New" stage to "Qualified" stage via kanban drag or form selector.
No distractors, no conversion wizard, no complex actions.
"""

TARGET_PARTNER = "Acme Corporation"
TARGET_EMAIL = "contact@acme.com"


def setup(env):
    # --- Cleanup prior runs ---
    env["crm.lead"].search([("partner_name", "=", TARGET_PARTNER)]).unlink()

    # --- Ensure required stages exist ---
    new_stage = env["crm.stage"].search([("name", "=", "New")], limit=1)
    if not new_stage:
        new_stage = env["crm.stage"].create({
            "name": "New",
            "sequence": 1,
        })

    qualified_stage = env["crm.stage"].search([("name", "=", "Qualified")], limit=1)
    if not qualified_stage:
        qualified_stage = env["crm.stage"].create({
            "name": "Qualified",
            "sequence": 2,
        })

    # --- Get sales team and user ---
    sales_team = env["crm.team"].search([("name", "=", "Sales")], limit=1)
    admin = env["res.users"].search([("login", "=", "admin")], limit=1)

    # --- Create the target opportunity in "New" stage ---
    env["crm.lead"].create({
        "name": TARGET_PARTNER,
        "partner_name": TARGET_PARTNER,
        "contact_name": "John Doe",
        "email_from": TARGET_EMAIL,
        "phone": "+1 555 0100",
        "type": "opportunity",
        "stage_id": new_stage.id,
        "expected_revenue": 50000.0,
        "team_id": sales_team.id if sales_team else False,
        "user_id": admin.id if admin else False,
        "description": "Opportunity for Acme Corporation — move to Qualified.",
    })
