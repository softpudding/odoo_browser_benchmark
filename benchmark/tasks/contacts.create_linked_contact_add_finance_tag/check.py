"""Postcondition checks for contacts.create_linked_contact_add_finance_tag."""


def check(env):
    failures = []

    contacts = env["res.partner"].search([("name", "=", "Dana Patel")])
    if len(contacts) != 1:
        return [f"Expected exactly 1 'Dana Patel' contact, found {len(contacts)}"]

    contact = contacts[0]
    if contact.is_company:
        failures.append("Dana Patel was created as a company, expected a person contact")
    if not contact.parent_id or contact.parent_id.name != "Lakeshore Manufacturing":
        actual = contact.parent_id.name if contact.parent_id else None
        failures.append(
            f"Parent company is '{actual}', expected 'Lakeshore Manufacturing'"
        )
    if contact.type != "contact":
        failures.append(f"Contact type is '{contact.type}', expected 'contact'")
    if contact.function != "Accounts Payable Specialist":
        failures.append(
            f"Job Position is '{contact.function}', expected 'Accounts Payable Specialist'"
        )
    if contact.email != "dana.patel@lakeshore.example.com":
        failures.append(
            f"Email is '{contact.email}', expected 'dana.patel@lakeshore.example.com'"
        )
    if contact.phone != "+1 312 555 0184":
        failures.append(
            f"Phone is '{contact.phone}', expected '+1 312 555 0184'"
        )
    if contact.street != "88 Harbor Way":
        failures.append(
            f"Street is '{contact.street}', expected '88 Harbor Way'"
        )
    if contact.city != "Chicago":
        failures.append(f"City is '{contact.city}', expected 'Chicago'")
    if contact.zip != "60601":
        failures.append(f"ZIP is '{contact.zip}', expected '60601'")
    if not contact.state_id or contact.state_id.code != "IL":
        actual = contact.state_id.code if contact.state_id else None
        failures.append(f"State is '{actual}', expected 'IL'")
    if not contact.country_id or contact.country_id.code != "US":
        failures.append("Country should be United States")

    tag_names = contact.category_id.mapped("name")
    if "Finance" not in tag_names:
        failures.append(f"Tags are {tag_names}, expected 'Finance' to be present")

    if contact.parent_id and contact.parent_id.name == "Lakeshore Manufacturing East":
        failures.append("Contact was linked to the distractor company")

    return failures
