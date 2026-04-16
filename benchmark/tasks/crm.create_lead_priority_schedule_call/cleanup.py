"""Cleanup for crm.create_lead_priority_schedule_call."""


def cleanup(env):
    leads = env["crm.lead"].search([
        ("name", "in", ["Apex Warehouse Expansion", "Apex Warehouse Renewal"]),
    ])
    if leads:
        env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "in", leads.ids),
        ]).unlink()
        leads.unlink()
    env["mail.activity"].search([("summary", "=", "Qualify warehouse rollout")]).unlink()
