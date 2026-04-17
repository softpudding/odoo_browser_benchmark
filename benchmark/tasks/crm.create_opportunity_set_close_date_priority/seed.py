"""Seed CRM data for crm.create_opportunity_set_close_date_priority."""

TARGET_NAME = "Vertex Renewal Expansion"


def setup(env):
    env["crm.lead"].search([("name", "=", TARGET_NAME)]).unlink()
    partner = env["res.partner"].search([("name", "=", "Azure Interior")], limit=1)
    if not partner:
        env["res.partner"].create({
            "name": "Azure Interior",
            "email": "sales@azure-interior.example.com",
        })
