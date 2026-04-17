"""Postcondition checks for crm.create_lead_priority_schedule_call."""

from datetime import date


def check(env):
    failures = []

    leads = env["crm.lead"].search([("name", "=", "Apex Warehouse Expansion")])
    if len(leads) != 1:
        return [f"Expected exactly 1 lead named 'Apex Warehouse Expansion', found {len(leads)}"]

    lead = leads[0]
    if lead.type != "lead":
        failures.append(f"Record type is '{lead.type}', expected 'lead'")
    if lead.priority != "2":
        failures.append(f"Priority is '{lead.priority}', expected '2'")

    activities = env["mail.activity"].search([
        ("res_model", "=", "crm.lead"),
        ("res_id", "=", lead.id),
        ("summary", "=", "Qualify warehouse rollout"),
    ])
    if len(activities) != 1:
        failures.append(
            f"Expected exactly 1 matching activity on the lead, found {len(activities)}"
        )
    else:
        activity = activities[0]
        if activity.activity_type_id.name != "Call":
            failures.append(
                f"Activity type is '{activity.activity_type_id.name}', expected 'Call'"
            )
        if activity.date_deadline != date(2026, 6, 15):
            failures.append(
                f"Activity due date is {activity.date_deadline}, expected 2026-06-15"
            )

    if lead.type != "lead":
        failures.append("Lead was converted to opportunity")

    distractor = env["crm.lead"].search([("name", "=", "Apex Warehouse Renewal")], limit=1)
    if not distractor:
        failures.append("Distractor lead 'Apex Warehouse Renewal' not found")
    elif distractor.priority != "0":
        failures.append("Distractor lead priority should stay unchanged")

    if env["sale.order"].search([("opportunity_id", "=", lead.id)], limit=1):
        failures.append("No quotation should have been created from the new lead")

    return failures
