"""Postcondition checks for contacts.create_company_add_supplier_finance_tags."""


TARGET_NAME = "Harborview Components"
DISTRACTOR_NAME = "Harborview Component Services"


def check(env):
    failures = []

    companies = env["res.partner"].search([
        ("name", "=", TARGET_NAME),
        ("is_company", "=", True),
    ])
    if len(companies) != 1:
        return [f"Expected exactly 1 company named '{TARGET_NAME}', found {len(companies)}"]

    company = companies[0]
    if company.phone != "+1 (415) 555-0148":
        failures.append(
            f"Phone is {company.phone!r}, expected '+1 (415) 555-0148'"
        )
    if not company.website or "harborview-components" not in company.website:
        failures.append(
            f"Website is {company.website!r}, expected a harborview-components URL"
        )
    tags = set(company.category_id.mapped("name"))
    if "Supplier" not in tags:
        failures.append(f"Company tags are {sorted(tags)!r}, expected Supplier")
    if company.child_ids:
        failures.append("No child contacts should have been created")

    distractor = env["res.partner"].search([
        ("name", "=", DISTRACTOR_NAME),
        ("is_company", "=", True),
    ], limit=1)
    if not distractor:
        failures.append(f"Distractor company '{DISTRACTOR_NAME}' not found")
    else:
        if distractor.phone != "+1 (415) 555-0102":
            failures.append(
                f"Distractor phone is {distractor.phone!r}, expected '+1 (415) 555-0102'"
            )

    return failures
