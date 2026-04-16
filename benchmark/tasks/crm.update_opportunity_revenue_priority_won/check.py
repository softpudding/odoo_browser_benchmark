"""Postcondition checks for crm.update_opportunity_revenue_priority_won."""

TARGET_NAME = "Northwind Renewal Review"
DISTRACTOR_NAME = "Northwind Renewal Pilot"


def check(env):
    failures = []

    lead_env = env["crm.lead"].with_context(active_test=False)
    target = lead_env.search([("name", "=", TARGET_NAME)], limit=1)
    distractor = lead_env.search([("name", "=", DISTRACTOR_NAME)], limit=1)

    if not target:
        return [f"Target opportunity {TARGET_NAME!r} not found"]
    if not distractor:
        return [f"Distractor opportunity {DISTRACTOR_NAME!r} not found"]

    if float(target.expected_revenue or 0.0) != 21000.0:
        failures.append(
            f"{TARGET_NAME} expected revenue is {target.expected_revenue}, expected 21000"
        )
    if target.priority != "2":
        failures.append(
            f"{TARGET_NAME} priority is {target.priority!r}, expected '2'"
        )
    if target.won_status != "won":
        failures.append(
            f"{TARGET_NAME} won_status is {target.won_status!r}, expected 'won'"
        )

    if float(distractor.expected_revenue or 0.0) != 9200.0:
        failures.append(
            f"{DISTRACTOR_NAME} expected revenue is {distractor.expected_revenue}, expected 9200"
        )
    if distractor.priority != "0":
        failures.append(
            f"{DISTRACTOR_NAME} priority is {distractor.priority!r}, expected '0'"
        )
    if distractor.won_status == "won":
        failures.append(f"{DISTRACTOR_NAME} was incorrectly marked won")

    return failures
