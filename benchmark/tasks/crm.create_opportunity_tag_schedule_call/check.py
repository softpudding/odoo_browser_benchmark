"""Postcondition checks for crm.create_opportunity_tag_schedule_call."""

from datetime import date


def check(env):
    failures = []

    partner = env["res.partner"].search([("name", "=", "Azure Interior")], limit=1)
    if not partner:
        return ["Partner 'Azure Interior' not found"]

    leads = env["crm.lead"].search([
        ("name", "=", "Vertex Renewal Expansion"),
    ])
    if len(leads) != 1:
        return [
            f"Expected exactly 1 opportunity named 'Vertex Renewal Expansion', found {len(leads)}"
        ]

    lead = leads[0]
    if lead.type != "opportunity":
        failures.append(f"Record type is '{lead.type}', expected 'opportunity'")
    if lead.partner_id.id != partner.id:
        failures.append(
            f"Customer is '{lead.partner_id.name}', expected 'Azure Interior'"
        )
    if float(lead.expected_revenue or 0.0) != 42000.0:
        failures.append(
            f"Expected revenue is {lead.expected_revenue}, expected 42000"
        )
    if float(lead.probability or 0.0) != 55.0:
        failures.append(
            f"Probability is {lead.probability}, expected 55"
        )
    if "Upsell" not in lead.tag_ids.mapped("name"):
        failures.append("Upsell tag was not added to the opportunity")

    activities = env["mail.activity"].search([
        ("res_model", "=", "crm.lead"),
        ("res_id", "=", lead.id),
        ("summary", "=", "Review renewal options"),
    ])
    if not activities:
        failures.append("Expected Call activity was not scheduled")
    else:
        activity = activities[0]
        if activity.activity_type_id.name != "Call":
            failures.append(
                f"Activity type is '{activity.activity_type_id.name}', expected 'Call'"
            )
        if activity.date_deadline != date(2026, 5, 13):
            failures.append(
                f"Activity due date is {activity.date_deadline}, expected 2026-05-13"
            )

    quotations = env["sale.order"].search([("opportunity_id", "=", lead.id)])
    if quotations:
        failures.append("No quotation should have been created from the opportunity")

    return failures
