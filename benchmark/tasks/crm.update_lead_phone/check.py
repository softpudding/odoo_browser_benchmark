"""Postcondition checks for crm.update_lead_phone."""

LEAD_NAME = "Summit Energy Expansion"


def check(env):
    failures = []

    lead = env["crm.lead"].search([
        ("name", "=", LEAD_NAME),
        ("type", "=", "lead"),
    ], limit=1)
    if not lead:
        return [f"Lead '{LEAD_NAME}' not found"]

    if (lead.phone or "") != "+1 555 0222":
        failures.append(f"Phone is '{lead.phone}', expected '+1 555 0222'")

    if lead.type != "lead":
        failures.append(f"Record type is '{lead.type}', expected 'lead'")

    return failures
