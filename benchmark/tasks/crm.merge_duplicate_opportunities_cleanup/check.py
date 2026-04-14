"""Postcondition checks for crm.merge_duplicate_opportunities_cleanup."""


TARGET_EMAIL = "renewal@northwind.example.com"
DISTRACTOR_NAME = "Westwind Logistics Renewal"
TARGET_ACTIVITY = "Northwind duplicate cleanup"


def check(env):
    failures = []

    merged = env["crm.lead"].search([("email_from", "=", TARGET_EMAIL)])
    distractor = env["crm.lead"].search([("name", "=", DISTRACTOR_NAME)], limit=1)

    if len(merged) != 1 or not distractor:
        return ["Expected 1 merged Northwind opportunity and 1 untouched Westwind opportunity"]

    opp = merged[0]
    if opp.type != "opportunity":
        failures.append(f"Merged record type is {opp.type!r}, expected 'opportunity'")
    if opp.partner_name != "Northwind Advisory":
        failures.append(f"Merged partner name is {opp.partner_name!r}, expected 'Northwind Advisory'")
    if opp.stage_id.name != "Qualified":
        failures.append(f"Merged stage is {opp.stage_id.name!r}, expected 'Qualified'")
    if float(opp.expected_revenue or 0.0) != 24000.0:
        failures.append(
            f"Merged expected revenue is {opp.expected_revenue!r}, expected 24000.0"
        )

    activities = env["mail.activity"].search([
        ("summary", "=", TARGET_ACTIVITY),
        ("res_model", "=", "crm.lead"),
        ("res_id", "=", opp.id),
    ])
    if len(activities) != 1:
        failures.append(f"Expected exactly 1 cleanup activity, found {len(activities)}")
    else:
        activity = activities[0]
        if activity.activity_type_id.name != "Call":
            failures.append(
                f"Cleanup activity type is {activity.activity_type_id.name!r}, expected 'Call'"
            )
        if str(activity.date_deadline) != "2026-05-08":
            failures.append(
                f"Cleanup activity due date is {activity.date_deadline!r}, expected '2026-05-08'"
            )

    if distractor.stage_id.name != "New":
        failures.append(
            f"Distractor stage is {distractor.stage_id.name!r}, expected to remain 'New'"
        )
    if env["mail.activity"].search_count([
        ("summary", "=", TARGET_ACTIVITY),
        ("res_model", "=", "crm.lead"),
        ("res_id", "=", distractor.id),
    ]):
        failures.append("Distractor opportunity received the cleanup activity")

    return failures
