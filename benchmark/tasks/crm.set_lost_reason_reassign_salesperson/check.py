"""Postcondition checks for crm.set_lost_reason_reassign_salesperson."""

OPP_NAME = "Acme – Q3 renewal"
LOST_REASON = "Too expensive"
EXPECTED_SALESPERSON = "Mitchell Admin"


def check(env):
    failures = []
    leads = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", OPP_NAME),
    ])
    if not leads:
        return [f"Opportunity '{OPP_NAME}' not found"]
    lead = leads[0]
    if lead.active:
        failures.append("Opportunity is still active — expected archived (Lost)")
    if not lead.lost_reason_id or lead.lost_reason_id.name != LOST_REASON:
        failures.append(
            f"lost_reason is '{lead.lost_reason_id.name if lead.lost_reason_id else None}', "
            f"expected '{LOST_REASON}'"
        )
    if not lead.user_id or lead.user_id.name != EXPECTED_SALESPERSON:
        failures.append(
            f"Salesperson is '{lead.user_id.name if lead.user_id else None}', "
            f"expected '{EXPECTED_SALESPERSON}'"
        )
    return failures
