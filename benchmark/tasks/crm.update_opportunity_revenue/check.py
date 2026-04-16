"""Postcondition checks for crm.update_opportunity_revenue."""

OPP_NAME = "BENCH-OPP-REV-01"
TARGET_REVENUE = 12500.0


def check(env):
    failures = []

    opp = env["crm.lead"].search([("name", "=", OPP_NAME)], limit=1)
    if not opp:
        return [f"Opportunity '{OPP_NAME}' not found"]

    if abs(float(opp.expected_revenue or 0.0) - TARGET_REVENUE) > 0.01:
        failures.append(
            f"Expected Revenue is '{opp.expected_revenue}', expected '{TARGET_REVENUE}'"
        )

    return failures
