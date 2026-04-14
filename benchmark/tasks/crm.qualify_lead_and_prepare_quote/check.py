"""Postcondition checks for crm.qualify_lead_and_prepare_quote."""


TARGET_NAME = "Northwind Advisory Platform Rollout"
WEST_NAME = "Northwind Advisory Renewal Follow-up"
TARGET_PARTNER = "Northwind Advisory East"
TARGET_TAG = "Executive Review"
TARGET_ACTIVITY = "Northwind discovery handoff"
TARGET_REF = "CRM-HANDOFF-24"


def check(env):
    failures = []

    lead = env["crm.lead"].search([("name", "=", TARGET_NAME)], limit=1)
    west = env["crm.lead"].search([("name", "=", WEST_NAME)], limit=1)
    if not lead or not west:
        return ["Missing seeded CRM leads for qualification handoff task"]

    if lead.type != "opportunity":
        failures.append(f"Target lead type is {lead.type!r}, expected 'opportunity'")
    if lead.partner_id.name != TARGET_PARTNER:
        failures.append(
            f"Target lead partner is {lead.partner_id.name!r}, expected {TARGET_PARTNER!r}"
        )
    if lead.stage_id.name != "Qualified":
        failures.append(f"Target lead stage is {lead.stage_id.name!r}, expected 'Qualified'")
    if float(lead.expected_revenue or 0.0) != 24000.0:
        failures.append(
            f"Target lead expected revenue is {lead.expected_revenue!r}, expected 24000.0"
        )
    if TARGET_TAG not in set(lead.tag_ids.mapped("name")):
        failures.append(f"Target lead is missing tag {TARGET_TAG!r}")

    activities = env["mail.activity"].search([
        ("summary", "=", TARGET_ACTIVITY),
        ("res_model", "=", "crm.lead"),
        ("res_id", "=", lead.id),
    ])
    if len(activities) != 1:
        failures.append(f"Expected exactly 1 target activity, found {len(activities)}")
    else:
        activity = activities[0]
        if activity.activity_type_id.name != "Call":
            failures.append(
                f"Activity type is {activity.activity_type_id.name!r}, expected 'Call'"
            )
        if str(activity.date_deadline) != "2026-05-06":
            failures.append(
                f"Activity due date is {activity.date_deadline!r}, expected '2026-05-06'"
            )

    quotes = env["sale.order"].search([("client_order_ref", "=", TARGET_REF)])
    if len(quotes) != 1:
        failures.append(f"Expected exactly 1 target quotation, found {len(quotes)}")
    else:
        quote = quotes[0]
        if quote.partner_id.name != TARGET_PARTNER:
            failures.append(
                f"Quotation customer is {quote.partner_id.name!r}, expected {TARGET_PARTNER!r}"
            )
        if quote.opportunity_id.id != lead.id:
            failures.append("Quotation is not linked to the target opportunity")
        if quote.state != "draft":
            failures.append(f"Quotation state is {quote.state!r}, expected 'draft'")
        if str(quote.validity_date) != "2026-05-20":
            failures.append(
                f"Quotation expiration is {quote.validity_date!r}, expected '2026-05-20'"
            )

    if west.type != "lead":
        failures.append(f"West lead type is {west.type!r}, expected to remain 'lead'")
    if env["sale.order"].search_count([("opportunity_id", "=", west.id)]):
        failures.append("West lead has quotation(s), expected none")

    return failures
