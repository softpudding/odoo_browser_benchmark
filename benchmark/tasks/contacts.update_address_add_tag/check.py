"""Postcondition checks for contacts.update_address_add_tag.

Validates:
1. Contact "Brookfield Dynamics" exists
2. Address fields updated correctly
3. Tag "Supplier" is present
4. Job position set to "Procurement Partner"
5. Name and email unchanged
"""

COMPANY_NAME = "Brookfield Dynamics"


def check(env):
    failures = []

    partner = env["res.partner"].search(
        [("name", "=", COMPANY_NAME)], limit=1
    )
    if not partner:
        return [f"Contact '{COMPANY_NAME}' not found"]

    # Check address
    if partner.street != "742 Innovation Blvd":
        failures.append(
            f"Street is '{partner.street}', expected '742 Innovation Blvd'"
        )
    if partner.city != "Portland":
        failures.append(f"City is '{partner.city}', expected 'Portland'")
    if partner.zip != "97201":
        failures.append(f"ZIP is '{partner.zip}', expected '97201'")

    # Check state (Oregon)
    if partner.state_id:
        if partner.state_id.name != "Oregon" and partner.state_id.code != "OR":
            failures.append(
                f"State is '{partner.state_id.name}', expected 'Oregon'"
            )
    else:
        failures.append("State not set, expected 'Oregon'")

    # Check country
    if not partner.country_id or partner.country_id.code != "US":
        failures.append("Country should be United States")

    # Check tag
    tag_names = partner.category_id.mapped("name")
    if "Supplier" not in tag_names:
        failures.append(
            f"Tags are {tag_names}, expected 'Supplier' to be present"
        )

    # Check job position
    if partner.function != "Procurement Partner":
        failures.append(
            f"Job position is '{partner.function}', expected 'Procurement Partner'"
        )

    # Check unchanged fields
    if partner.email != "info@brookfielddynamics.com":
        failures.append(
            f"Email changed to '{partner.email}', should remain 'info@brookfielddynamics.com'"
        )

    return failures
