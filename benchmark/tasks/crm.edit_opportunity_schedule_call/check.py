"""Postcondition checks for crm.edit_opportunity_schedule_call.

Validates:
1. Opportunity "Beacon Analytics Deal" exists
2. Expected revenue is 75000
3. Probability is 60
4. A Call activity is scheduled for 2026-05-10 with correct summary
5. Stage unchanged (still Qualified)
"""

from datetime import date


def check(env):
    failures = []

    opp = env["crm.lead"].search([
        ("name", "=", "Beacon Analytics Deal"),
        ("type", "=", "opportunity"),
    ], limit=1)

    if not opp:
        return ["Opportunity 'Beacon Analytics Deal' not found"]

    # Check revenue
    if float(opp.expected_revenue) != 75000.0:
        failures.append(
            f"Expected revenue is {opp.expected_revenue}, expected 75000"
        )

    # Check probability
    if float(opp.probability) != 60.0:
        failures.append(
            f"Probability is {opp.probability}, expected 60"
        )

    # Check stage unchanged
    if opp.stage_id.name != "Qualified":
        failures.append(
            f"Stage changed to '{opp.stage_id.name}', expected 'Qualified'"
        )

    # Check activity
    activities = env["mail.activity"].search([
        ("res_model", "=", "crm.lead"),
        ("res_id", "=", opp.id),
    ])

    call_activities = activities.filtered(
        lambda a: a.activity_type_id.name == "Call"
    )

    if not call_activities:
        # Also check by category for Odoo 19 compatibility
        call_activities = activities.filtered(
            lambda a: a.activity_type_id.category == "phonecall"
            or "call" in (a.activity_type_id.name or "").lower()
        )

    if not call_activities:
        failures.append("No Call activity found on the opportunity")
    else:
        act = call_activities[0]
        expected_date = date(2026, 5, 10)
        if act.date_deadline != expected_date:
            failures.append(
                f"Activity due date is {act.date_deadline}, expected {expected_date}"
            )
        if act.summary and "Follow up on proposal" not in act.summary:
            failures.append(
                f"Activity summary is '{act.summary}', expected 'Follow up on proposal'"
            )
        elif not act.summary:
            failures.append("Activity summary is empty, expected 'Follow up on proposal'")

    return failures
