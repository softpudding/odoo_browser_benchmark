"""Seed a CRM opportunity for the priority-setting task.

Category: deep_ui_interaction (EASY).
Starting state: Opportunity "Beacon Analytics Deal" in "New" stage with
priority 0 (normal). The agent must set priority to 2.
"""


def setup(env):
    # --- Cleanup prior runs ---
    env["crm.lead"].search([("name", "=", "Beacon Analytics Deal")]).unlink()

    # --- Ensure required stage exists ---
    new_stage = env["crm.stage"].search([("name", "=", "New")], limit=1)
    if not new_stage:
        new_stage = env["crm.stage"].create({
            "name": "New",
            "sequence": 1,
        })

    # --- Get sales team and user ---
    sales_team = env["crm.team"].search([("name", "=", "Sales")], limit=1)
    admin = env["res.users"].search([("login", "=", "admin")], limit=1)

    # --- Create the target opportunity ---
    env["crm.lead"].create({
        "name": "Beacon Analytics Deal",
        "partner_name": "Beacon Analytics",
        "contact_name": "Jane Smith",
        "email_from": "jane.smith@beaconanalytics.com",
        "phone": "+1 555 0300",
        "type": "opportunity",
        "stage_id": new_stage.id,
        "expected_revenue": 80000.0,
        "priority": "0",
        "team_id": sales_team.id if sales_team else False,
        "user_id": admin.id if admin else False,
        "description": "Analytics platform deal — set priority to Important.",
    })
