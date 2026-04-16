"""Postcondition checks for crm.move_opportunity_stage.

Validates that:
1. The target opportunity "Acme Corporation" exists
2. Its stage changed to "Qualified"
3. Expected revenue remains unchanged at 50000
"""

TARGET_PARTNER = "Acme Corporation"
TARGET_EMAIL = "contact@acme.com"
EXPECTED_REVENUE = 50000.0


def check(env):
    failures = []

    # Find the target opportunity
    opp = env["crm.lead"].search([
        ("partner_name", "=", TARGET_PARTNER),
        ("type", "=", "opportunity"),
    ], limit=1)

    if not opp:
        return [f"Opportunity '{TARGET_PARTNER}' not found"]

    # Check stage is "Qualified"
    if not opp.stage_id:
        failures.append("Opportunity has no stage assigned")
    elif opp.stage_id.name != "Qualified":
        failures.append(
            f"Opportunity stage is '{opp.stage_id.name}', expected 'Qualified'"
        )

    # Check expected revenue unchanged
    actual_revenue = float(opp.expected_revenue or 0.0)
    if actual_revenue != EXPECTED_REVENUE:
        failures.append(
            f"Expected revenue is {actual_revenue}, expected {EXPECTED_REVENUE}"
        )

    # Check type is still opportunity
    if opp.type != "opportunity":
        failures.append(
            f"Record type is '{opp.type}', expected 'opportunity'"
        )

    return failures
