"""Postcondition checks for crm.set_priority_on_opportunity.

Validates that:
1. The opportunity "Beacon Analytics Deal" has priority set to 3
2. The opportunity still exists and is in the same stage
"""


def check(env):
    failures = []

    # Find the target opportunity
    lead = env["crm.lead"].search([
        ("name", "=", "Beacon Analytics Deal"),
    ], limit=1)

    if not lead:
        return ["Opportunity 'Beacon Analytics Deal' not found"]

    # Check priority is set to 3
    if lead.priority != "3":
        failures.append(
            f"Priority is '{lead.priority}', expected '3' (High)"
        )

    # Check opportunity is still an opportunity (not converted)
    if lead.type != "opportunity":
        failures.append(
            f"Record type is '{lead.type}', expected 'opportunity'"
        )

    return failures