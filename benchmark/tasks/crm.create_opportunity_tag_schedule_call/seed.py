"""Seed CRM data for the create-opportunity-tag-schedule-call task.

Category 2 (MEDIUM): create a new opportunity from scratch, fill several
fields, then schedule one activity without branching into quotation creation.
"""

TARGET_NAME = "Vertex Renewal Expansion"
TARGET_TAG = "Upsell"
TARGET_ACTIVITY = "Review renewal options"


def setup(env):
    leads = env["crm.lead"].search([("name", "=", TARGET_NAME)])
    for lead in leads:
        env["mail.activity"].search([
            ("res_model", "=", "crm.lead"),
            ("res_id", "=", lead.id),
        ]).unlink()
        lead.unlink()

    env["mail.activity"].search([("summary", "=", TARGET_ACTIVITY)]).unlink()

    partner = env["res.partner"].search([("name", "=", "Azure Interior")], limit=1)
    if not partner:
        env["res.partner"].create({
            "name": "Azure Interior",
            "email": "sales@azure-interior.example.com",
        })

    tag = env["crm.tag"].search([("name", "=", TARGET_TAG)], limit=1)
    if not tag:
        env["crm.tag"].create({"name": TARGET_TAG})
