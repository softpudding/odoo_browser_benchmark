"""Postcondition checks for crm.convert_lead_qualify."""


LEAD_NAME = "Silver Maple Network Refresh"
LEAD_EMAIL = "ops+netops@silvermaple.example.com"
DISTRACTOR_NAME = "Silver Maple Network Review"
DISTRACTOR_EMAIL = "ops+review@silvermaple.example.com"


def check(env):
    failures = []

    lead = env["crm.lead"].search([
        ("name", "=", LEAD_NAME),
        ("email_from", "=", LEAD_EMAIL),
    ], limit=1)
    if not lead:
        return [f"Lead '{LEAD_NAME}' not found"]

    if lead.type != "opportunity":
        failures.append(f"Lead type is '{lead.type}', expected 'opportunity'")
    if lead.stage_id.name != "Qualified":
        failures.append(
            f"Lead stage is '{lead.stage_id.name}', expected 'Qualified'"
        )

    quotations = env["sale.order"].search([("opportunity_id", "=", lead.id)])
    if quotations:
        failures.append("A quotation was created, but the task must stay in CRM only")

    distractor = env["crm.lead"].search([
        ("name", "=", DISTRACTOR_NAME),
        ("email_from", "=", DISTRACTOR_EMAIL),
    ], limit=1)
    if not distractor:
        failures.append("Distractor lead not found")
    else:
        if distractor.type != "lead":
            failures.append(
                f"Distractor lead type is '{distractor.type}', expected 'lead'"
            )
        if distractor.stage_id.name == "Qualified":
            failures.append("Distractor lead was moved to Qualified unexpectedly")

    return failures
