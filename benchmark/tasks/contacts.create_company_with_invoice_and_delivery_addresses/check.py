"""Postcondition checks for contacts.create_company_with_invoice_and_delivery_addresses."""


def check(env):
    failures = []

    company = env["res.partner"].search([("name", "=", "Harbor Peak Logistics"), ("is_company", "=", True)], limit=1)
    if not company:
        return ["Company 'Harbor Peak Logistics' not found"]

    if company.phone != "+1 (503) 555-0140":
        failures.append(f"Company phone is {company.phone!r}")
    if not company.website or "harborpeak-logistics" not in company.website:
        failures.append(f"Company website is {company.website!r}")
    if company.street != "820 Rivergate Ave":
        failures.append(f"Company street is {company.street!r}")
    if company.city != "Portland":
        failures.append(f"Company city is {company.city!r}")
    if company.zip != "97217":
        failures.append(f"Company ZIP is {company.zip!r}")
    if not company.country_id or company.country_id.name != "United States":
        failures.append(f"Company country is {(company.country_id.name if company.country_id else None)!r}")

    invoice = env["res.partner"].search([("name", "=", "Billing Desk"), ("type", "=", "invoice")], limit=1)
    if not invoice:
        failures.append("Invoice child address 'Billing Desk' not found")
    else:
        if invoice.parent_id != company:
            failures.append("Billing Desk is not linked to Harbor Peak Logistics")
        if invoice.street != "825 Rivergate Ave":
            failures.append(f"Billing Desk street is {invoice.street!r}")
        if invoice.city != "Portland":
            failures.append(f"Billing Desk city is {invoice.city!r}")
        if invoice.zip != "97217":
            failures.append(f"Billing Desk ZIP is {invoice.zip!r}")

    delivery = env["res.partner"].search([("name", "=", "Receiving Dock"), ("type", "=", "delivery")], limit=1)
    if not delivery:
        failures.append("Delivery child address 'Receiving Dock' not found")
    else:
        if delivery.parent_id != company:
            failures.append("Receiving Dock is not linked to Harbor Peak Logistics")
        if delivery.street != "910 Dockside Rd":
            failures.append(f"Receiving Dock street is {delivery.street!r}")
        if delivery.city != "Portland":
            failures.append(f"Receiving Dock city is {delivery.city!r}")
        if delivery.zip != "97217":
            failures.append(f"Receiving Dock ZIP is {delivery.zip!r}")

    return failures
