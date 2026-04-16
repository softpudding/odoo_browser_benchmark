"""Postcondition checks for contacts.create_company_with_supplier_tag."""


def check(env):
    failures = []

    companies = env["res.partner"].search([
        ("name", "=", "North Coast Fabrication"),
        ("is_company", "=", True),
    ])
    if len(companies) != 1:
        return [
            f"Expected exactly 1 company named 'North Coast Fabrication', found {len(companies)}"
        ]

    company = companies[0]
    if company.phone != "+1 (206) 555-0184":
        failures.append(
            f"Phone is '{company.phone}', expected '+1 (206) 555-0184'"
        )
    if not company.website or "northcoastfab" not in company.website:
        failures.append(
            f"Website is '{company.website}', expected a northcoastfab URL"
        )
    if company.street != "85 Harbor Way":
        failures.append(
            f"Street is '{company.street}', expected '85 Harbor Way'"
        )
    if company.city != "Seattle":
        failures.append(f"City is '{company.city}', expected 'Seattle'")
    if company.zip != "98134":
        failures.append(f"ZIP is '{company.zip}', expected '98134'")
    if not company.state_id or company.state_id.code != "WA":
        actual = company.state_id.code if company.state_id else None
        failures.append(f"State code is '{actual}', expected 'WA'")
    if not company.country_id or company.country_id.code != "US":
        actual = company.country_id.code if company.country_id else None
        failures.append(f"Country code is '{actual}', expected 'US'")
    if "Supplier" not in company.category_id.mapped("name"):
        failures.append("Supplier tag was not added to the company")
    if company.child_ids:
        failures.append("No linked child contacts should have been created")

    distractor = env["res.partner"].search([
        ("name", "=", "North Coast Fabricators"),
        ("is_company", "=", True),
    ], limit=1)
    if not distractor:
        failures.append("Distractor company 'North Coast Fabricators' not found")
    else:
        if "Supplier" in distractor.category_id.mapped("name"):
            failures.append("Distractor company received the Supplier tag")
        if distractor.phone != "+1 (206) 555-0110":
            failures.append(
                f"Distractor phone is '{distractor.phone}', expected '+1 (206) 555-0110'"
            )

    return failures
