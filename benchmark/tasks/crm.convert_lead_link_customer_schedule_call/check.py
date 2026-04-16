"""Postcondition checks for crm.convert_lead_link_customer_schedule_call."""


TARGET_NAME = "Summit Ridge Support Rollout"
DISTRACTOR_NAME = "Summit Ridge Support Review"
TARGET_CUSTOMER = "Summit Ridge Manufacturing"
TARGET_ACTIVITY = "Review support rollout scope"


def check(env):
    failures = []

    lead = env["crm.lead"].search([("name", "=", TARGET_NAME)], limit=1)
    distractor = env["crm.lead"].search([("name", "=", DISTRACTOR_NAME)], limit=1)
    if not lead or not distractor:
        return ["Missing seeded CRM leads for conversion task"]

    if lead.type != "opportunity":
        failures.append(f"Target lead type is {lead.type!r}, expected 'opportunity'")
    if lead.partner_id.name != TARGET_CUSTOMER:
        failures.append(
            f"Target opportunity partner is {lead.partner_id.name!r}, expected {TARGET_CUSTOMER!r}"
        )
    if float(lead.expected_revenue or 0.0) != 18000.0:
        failures.append(
            f"Expected revenue is {lead.expected_revenue!r}, expected 18000.0"
        )
    if lead.priority != "2":
        failures.append(f"Priority is {lead.priority!r}, expected '2'")
    if lead.stage_id.name != "Qualified":
        failures.append(f"Stage is {lead.stage_id.name!r}, expected 'Qualified'")

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
        if str(activity.date_deadline) != "2026-05-19":
            failures.append(
                f"Activity due date is {activity.date_deadline!r}, expected '2026-05-19'"
            )

    if distractor.type != "lead":
        failures.append(f"Distractor lead type is {distractor.type!r}, expected 'lead'")
    distractor_activities = env["mail.activity"].search([
        ("summary", "=", TARGET_ACTIVITY),
        ("res_model", "=", "crm.lead"),
        ("res_id", "=", distractor.id),
    ])
    if distractor_activities:
        failures.append("Distractor lead received the target activity")

    return failures
