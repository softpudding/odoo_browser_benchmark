"""Seed for contacts.create_company_with_invoice_and_delivery_addresses."""


def setup(env):
    for name in ["Harbor Peak Logistics", "Billing Desk", "Receiving Dock"]:
        env["res.partner"].search([("name", "=", name)]).unlink()
