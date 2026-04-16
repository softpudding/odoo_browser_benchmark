"""Postcondition checks for contacts.create_company_set_supplier_tag."""


COMPANY_NAME = "Harborview Fabrication"


def check(env):
    failures = []

    companies = env["res.partner"].search([("name", "=", COMPANY_NAME)])
    if len(companies) != 1:
        return [f"Expected exactly 1 company named '{COMPANY_NAME}', found {len(companies)}"]

    company = companies[0]
    if not company.is_company:
        failures.append("Created contact is not marked as a company")
    if company.email != "ops@harborview.example.com":
        failures.append(
            f"Email is '{company.email}', expected 'ops@harborview.example.com'"
        )
    if company.phone != "+1 206 555 0144":
        failures.append(
            f"Phone is '{company.phone}', expected '+1 206 555 0144'"
        )
    if company.website != "https://harborview.example.com":
        failures.append(
            f"Website is '{company.website}', expected 'https://harborview.example.com'"
        )

    tag_names = company.category_id.mapped("name")
    if tag_names != ["Supplier"]:
        failures.append(f"Tags are {tag_names}, expected ['Supplier']")

    return failures
