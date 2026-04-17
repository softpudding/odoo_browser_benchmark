"""Postcondition checks for crm.update_lead_email."""

LEAD_NAME = "Cobalt Cloud Expansion"
TARGET_EMAIL = "cobalt-expansion@cobaltcloud.example.com"


def check(env):
    failures = []

    lead = env["crm.lead"].search([
        ("name", "=", LEAD_NAME),
        ("type", "=", "lead"),
    ], limit=1)
    if not lead:
        return [f"Lead '{LEAD_NAME}' not found"]

    if (lead.email_from or "").strip() != TARGET_EMAIL:
        failures.append(
            f"Email is '{lead.email_from}', expected '{TARGET_EMAIL}'"
        )

    if lead.type != "lead":
        failures.append(f"Record type changed to '{lead.type}', expected 'lead'")

    return failures
