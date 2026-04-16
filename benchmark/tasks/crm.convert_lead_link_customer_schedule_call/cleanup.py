"""Cleanup for crm.convert_lead_link_customer_schedule_call."""


def cleanup(env):
    env["mail.activity"].search([("summary", "=", "Review support rollout scope")]).unlink()
    env["crm.lead"].search([
        ("name", "in", ["Summit Ridge Support Rollout", "Summit Ridge Support Review"]),
    ]).unlink()
