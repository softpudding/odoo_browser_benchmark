"""Postcondition checks for crm.create_opportunity_set_close_date_priority."""

from datetime import date


def check(env):
    failures = []
    partner = env["res.partner"].search([("name", "=", "Azure Interior")], limit=1)
    if not partner:
        return ["Partner 'Azure Interior' not found"]
    leads = env["crm.lead"].search([("name", "=", "Vertex Renewal Expansion")])
    if len(leads) != 1:
        return [f"Expected exactly 1 opportunity named 'Vertex Renewal Expansion', found {len(leads)}"]
    lead = leads[0]
    if lead.type != "opportunity":
        failures.append(f"Record type is '{lead.type}', expected 'opportunity'")
    if lead.partner_id.id != partner.id:
        failures.append(f"Customer is '{lead.partner_id.name}', expected 'Azure Interior'")
    if float(lead.expected_revenue or 0.0) != 42000.0:
        failures.append(f"Expected revenue is {lead.expected_revenue}, expected 42000")
    if lead.priority != "3":
        failures.append(f"Priority is '{lead.priority}', expected '3'")
    if lead.date_deadline != date(2026, 5, 20):
        failures.append(f"Expected closing date is {lead.date_deadline}, expected 2026-05-20")
    quotations = env["sale.order"].search([("opportunity_id", "=", lead.id)])
    if quotations:
        failures.append("No quotation should have been created from the opportunity")
    return failures
