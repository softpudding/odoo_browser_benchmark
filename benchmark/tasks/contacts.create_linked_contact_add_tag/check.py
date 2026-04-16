"""Postcondition checks for contacts.create_linked_contact_add_tag."""


def check(env):
    failures = []

    contacts = env["res.partner"].search([("name", "=", "Leah Morgan")])
    if len(contacts) != 1:
        return [f"Expected exactly 1 'Leah Morgan' contact, found {len(contacts)}"]

    contact = contacts[0]
    if contact.is_company:
        failures.append("Leah Morgan was created as a company, expected a person contact")
    if not contact.parent_id or contact.parent_id.name != "Seabird Logistics":
        failures.append(
            f"Parent company is '{contact.parent_id.name if contact.parent_id else None}', expected 'Seabird Logistics'"
        )
    if contact.function != "Operations Coordinator":
        failures.append(
            f"Job position is '{contact.function}', expected 'Operations Coordinator'"
        )
    if contact.email != "leah.morgan@seabird.example.com":
        failures.append(
            f"Email is '{contact.email}', expected 'leah.morgan@seabird.example.com'"
        )
    if contact.phone != "+1 415 555 0147":
        failures.append(
            f"Phone is '{contact.phone}', expected '+1 415 555 0147'"
        )

    if contact.parent_id and contact.parent_id.name == "Seabird Logistics West":
        failures.append("Contact was linked to the distractor company")

    return failures
