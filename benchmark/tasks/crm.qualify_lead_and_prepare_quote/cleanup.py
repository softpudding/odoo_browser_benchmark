"""Cleanup for crm.qualify_lead_and_prepare_quote."""


def cleanup(env):
    env["sale.order"].search([("client_order_ref", "=", "CRM-HANDOFF-24")]).unlink()
    env["mail.activity"].search([("summary", "=", "Northwind discovery handoff")]).unlink()
    env["crm.lead"].search([
        ("email_from", "in", ["ops-east@northwind.example.com", "ops-west@northwind.example.com"]),
    ]).unlink()
