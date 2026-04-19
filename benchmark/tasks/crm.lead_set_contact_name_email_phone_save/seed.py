"""Seed a bare CRM lead with empty contact_name/email_from/phone.

Easy task: agent must fill three char fields on a single form and save.
Tests that BU can:
  1. Navigate CRM -> Leads list (not Opportunities pipeline).
  2. Open the right lead (no distractor; the list is single-row).
  3. Fill three specific char fields in one form save.

The Leads menu is gated by `crm.group_use_lead`, so we enable it on admin
before seeding.
"""

LEAD_NAME = "Bench Lead Basic"
TEAM_NAME = "Sales"
USER_LOGIN = "admin"


def setup(env):
    # --- Enable the Leads feature for admin so the Leads menu is visible ---
    group_lead = env.ref("crm.group_use_lead", raise_if_not_found=False)
    if group_lead:
        admin_user = env.ref("base.user_admin", raise_if_not_found=False)
        if admin_user and group_lead not in admin_user.group_ids:
            admin_user.write({"group_ids": [(4, group_lead.id)]})

    # --- Cleanup prior runs ---
    old = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", LEAD_NAME),
    ])
    if old:
        env["mail.message"].search([
            ("model", "=", "crm.lead"),
            ("res_id", "in", old.ids),
        ]).unlink()
        env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "in", old.ids),
        ]).unlink()
        old.unlink()

    team = env["crm.team"].search([("name", "=", TEAM_NAME)], limit=1)
    if not team:
        team = env["crm.team"].create({"name": TEAM_NAME})

    admin = env["res.users"].search([("login", "=", USER_LOGIN)], limit=1)

    env["crm.lead"].create({
        "name": LEAD_NAME,
        "type": "lead",
        "contact_name": False,
        "email_from": False,
        "phone": False,
        "team_id": team.id,
        "user_id": admin.id if admin else False,
        "description": "Raw lead that needs contact details filled in.",
    })
