"""Postcondition checks for crm.assign_lead_salesperson_change_stage_won.

Validates:
1. Opportunity 'Bench Big Deal' still exists and is active.
2. user_id equals 'Bench Rep'.
3. stage_id.name equals 'Won' (is_won=True).
4. probability == 100.
5. Expected revenue is still 50000 and partner is still 'Bench Buyer Co'.
"""

OPP_NAME = "Bench Big Deal"
EXPECTED_REP = "Bench Rep"
EXPECTED_PARTNER = "Bench Buyer Co"
EXPECTED_REVENUE = 50000.0


def check(env):
    failures = []

    leads = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", OPP_NAME),
    ])
    if not leads:
        return [f"Opportunity '{OPP_NAME}' not found"]
    if len(leads) > 1:
        failures.append(
            f"Expected exactly one '{OPP_NAME}' opportunity, found {len(leads)}"
        )
    lead = leads[0]

    if not lead.active:
        failures.append("Opportunity is archived (active=False); expected active=True")

    if not lead.user_id or lead.user_id.name != EXPECTED_REP:
        actual = lead.user_id.name if lead.user_id else None
        failures.append(
            f"Salesperson is '{actual}', expected '{EXPECTED_REP}'"
        )

    stage_name = lead.stage_id.name if lead.stage_id else None
    if stage_name != "Won" or not (lead.stage_id and lead.stage_id.is_won):
        failures.append(
            f"Stage is '{stage_name}' (is_won={bool(lead.stage_id and lead.stage_id.is_won)}); "
            f"expected 'Won' with is_won=True"
        )

    if abs((lead.probability or 0.0) - 100.0) > 0.01:
        failures.append(
            f"Probability is {lead.probability}, expected 100"
        )

    # Guardrails — prompt forbids changing these
    if not lead.partner_id or lead.partner_id.name != EXPECTED_PARTNER:
        actual = lead.partner_id.name if lead.partner_id else None
        failures.append(
            f"Partner is '{actual}', expected '{EXPECTED_PARTNER}'"
        )
    if abs((lead.expected_revenue or 0.0) - EXPECTED_REVENUE) > 0.01:
        failures.append(
            f"Expected revenue is {lead.expected_revenue}, expected {EXPECTED_REVENUE}"
        )
    if lead.type != "opportunity":
        failures.append(
            f"Record type is '{lead.type}', expected 'opportunity'"
        )

    return failures
