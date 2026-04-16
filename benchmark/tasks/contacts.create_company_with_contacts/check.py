"""Postcondition checks for contacts.create_company_with_contacts.

Validates that:
1. The company 'Vantage Industrial Group' was created with correct fields
2. Two individual contacts were created and linked to the company
"""


def check(env):
    failures = []

    # --- Company checks ---
    company = env["res.partner"].search(
        [("name", "=", "Vantage Industrial Group"), ("is_company", "=", True)],
        limit=1,
    )
    if not company:
        return ["Company 'Vantage Industrial Group' not found (must be is_company=True)"]

    if company.phone != "+1 (312) 555-0190":
        failures.append(
            f"Company phone: expected '+1 (312) 555-0190', got '{company.phone}'"
        )
    if company.website and "vantage-industrial" not in (company.website or ""):
        failures.append(
            f"Company website: expected 'vantage-industrial.example.com', got '{company.website}'"
        )
    if company.street != "4400 Commerce Drive":
        failures.append(
            f"Company street: expected '4400 Commerce Drive', got '{company.street}'"
        )
    if company.city != "Chicago":
        failures.append(
            f"Company city: expected 'Chicago', got '{company.city}'"
        )
    if company.zip != "60609":
        failures.append(
            f"Company ZIP: expected '60609', got '{company.zip}'"
        )
    if not company.country_id or "United States" not in company.country_id.name:
        actual = company.country_id.name if company.country_id else "(none)"
        failures.append(
            f"Company country: expected 'United States', got '{actual}'"
        )

    # --- Individual contact: Patricia Drum ---
    patricia = env["res.partner"].search(
        [("name", "=", "Patricia Drum"), ("is_company", "=", False)], limit=1
    )
    if not patricia:
        failures.append("Contact 'Patricia Drum' not found")
    else:
        if not patricia.parent_id or patricia.parent_id.id != company.id:
            actual = patricia.parent_id.name if patricia.parent_id else "(none)"
            failures.append(
                f"Patricia Drum's company: expected 'Vantage Industrial Group', got '{actual}'"
            )
        if patricia.function != "Procurement Manager":
            failures.append(
                f"Patricia Drum's job position: expected 'Procurement Manager', got '{patricia.function}'"
            )
        if patricia.email != "p.drum@vantage-industrial.example.com":
            failures.append(
                f"Patricia Drum's email: expected 'p.drum@vantage-industrial.example.com', got '{patricia.email}'"
            )
        if patricia.phone != "+1 (312) 555-0191":
            failures.append(
                f"Patricia Drum's phone: expected '+1 (312) 555-0191', got '{patricia.phone}'"
            )

    # --- Individual contact: Steven Okafor ---
    steven = env["res.partner"].search(
        [("name", "=", "Steven Okafor"), ("is_company", "=", False)], limit=1
    )
    if not steven:
        failures.append("Contact 'Steven Okafor' not found")
    else:
        if not steven.parent_id or steven.parent_id.id != company.id:
            actual = steven.parent_id.name if steven.parent_id else "(none)"
            failures.append(
                f"Steven Okafor's company: expected 'Vantage Industrial Group', got '{actual}'"
            )
        if steven.function != "Logistics Coordinator":
            failures.append(
                f"Steven Okafor's job position: expected 'Logistics Coordinator', got '{steven.function}'"
            )
        if steven.email != "s.okafor@vantage-industrial.example.com":
            failures.append(
                f"Steven Okafor's email: expected 's.okafor@vantage-industrial.example.com', got '{steven.email}'"
            )
        if steven.phone != "+1 (312) 555-0192":
            failures.append(
                f"Steven Okafor's phone: expected '+1 (312) 555-0192', got '{steven.phone}'"
            )

    return failures
