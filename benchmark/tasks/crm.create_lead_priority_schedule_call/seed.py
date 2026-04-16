"""Seed data for crm.create_lead_priority_schedule_call."""

TARGET_NAME = "Apex Warehouse Expansion"
DISTRACTOR_NAME = "Apex Warehouse Renewal"
ACTIVITY_SUMMARY = "Qualify warehouse rollout"


def setup(env):
    group_lead = env.ref("crm.group_use_lead", raise_if_not_found=False)
    if group_lead:
        admin = env.ref("base.user_admin")
        if group_lead not in admin.group_ids:
            admin.write({"group_ids": [(4, group_lead.id)]})

    leads = env["crm.lead"].search([("name", "in", [TARGET_NAME, DISTRACTOR_NAME])])
    if leads:
        env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "in", leads.ids),
        ]).unlink()
        leads.unlink()

    env["mail.activity"].search([("summary", "=", ACTIVITY_SUMMARY)]).unlink()

    env["crm.lead"].create({
        "name": DISTRACTOR_NAME,
        "type": "lead",
        "contact_name": "Mina Foster",
        "email_from": "mina@apexwarehouse.com",
        "expected_revenue": 36000.0,
        "priority": "0",
    })
