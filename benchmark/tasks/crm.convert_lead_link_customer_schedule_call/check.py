"""Postcondition checks for crm.convert_lead_link_customer_schedule_call."""


TARGET_NAME = "Summit Ridge Support Rollout"
DISTRACTOR_NAME = "Summit Ridge Support Review"
TARGET_CUSTOMER = "Summit Ridge Manufacturing"
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
    if lead.stage_id.name != "Qualified":
        failures.append(f"Stage is {lead.stage_id.name!r}, expected 'Qualified'")

    if distractor.type != "lead":
        failures.append(f"Distractor lead type is {distractor.type!r}, expected 'lead'")

    return failures
