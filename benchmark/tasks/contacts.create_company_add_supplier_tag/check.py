"""Postcondition checks for contacts.create_company_add_supplier_tag."""


def check(env):
    failures = []

    companies = env["res.partner"].search([("name", "=", "North Coast Fabrication")])
    if len(companies) != 1:
        return [f"Expected exactly 1 target company, found {len(companies)}"]

    company = companies[0]
    if not company.is_company:
        failures.append("Target contact is not marked as a company")
    if company.street != "1450 Harbor Rd":
        failures.append(f"Street is '{company.street}', expected '1450 Harbor Rd'")
    if company.city != "Tacoma":
        failures.append(f"City is '{company.city}', expected 'Tacoma'")
    if company.zip != "98402":
        failures.append(f"ZIP is '{company.zip}', expected '98402'")
    if company.email != "ops@northcoastfab.com":
        failures.append(f"Email is '{company.email}', expected 'ops@northcoastfab.com'")
    if company.phone != "+1 555 0182":
        failures.append(f"Phone is '{company.phone}', expected '+1 555 0182'")
    if company.website != "https://northcoastfab.com":
        failures.append(
            f"Website is '{company.website}', expected 'https://northcoastfab.com'"
        )
    if "Supplier" not in company.category_id.mapped("name"):
        failures.append("Supplier tag is missing on target company")
    if company.child_ids:
        failures.append("Target company should not have child contacts")

    distractor = env["res.partner"].search([("name", "=", "North Coast Fabrication East")], limit=1)
    if not distractor:
        failures.append("Distractor company 'North Coast Fabrication East' not found")
    elif distractor.category_id:
        failures.append("Distractor company should not have any tags")

    return failures
