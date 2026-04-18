"""Postcondition checks for crm.assign_team_change_salesperson_log_activity.

Validates:
1. Opportunity 'Bench Big Deal' still exists.
2. team_id is now 'Channel'.
3. user_id (salesperson) is now 'Sara Sales'.
4. A Call activity is scheduled with date_deadline 2026-06-10 and summary
   containing 'Discovery call'.
"""

from datetime import date


OPP_NAME = "Bench Big Deal"
EXPECTED_TEAM = "Channel"
EXPECTED_SALESPERSON = "Sara Sales"
EXPECTED_SUMMARY = "Discovery call"
EXPECTED_DATE = date(2026, 6, 10)


def check(env):
    failures = []

    leads = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", OPP_NAME),
    ])
    if not leads:
        return [f"Opportunity '{OPP_NAME}' not found"]
    lead = leads[0]

    if not lead.team_id or lead.team_id.name != EXPECTED_TEAM:
        failures.append(
            f"Sales Team is '{lead.team_id.name if lead.team_id else None}', "
            f"expected '{EXPECTED_TEAM}'"
        )

    if not lead.user_id or lead.user_id.name != EXPECTED_SALESPERSON:
        failures.append(
            f"Salesperson is '{lead.user_id.name if lead.user_id else None}', "
            f"expected '{EXPECTED_SALESPERSON}'"
        )

    activities = env["mail.activity"].search([
        ("res_model", "=", "crm.lead"),
        ("res_id", "=", lead.id),
    ])

    call_activities = activities.filtered(
        lambda a: (a.activity_type_id.name or "").lower() == "call"
        or a.activity_type_id.category == "phonecall"
    )

    if not call_activities:
        failures.append(
            "No Call activity found on the opportunity"
        )
    else:
        # Prefer an activity that matches both date and summary if there are
        # multiple Call activities; otherwise use the first one.
        match = call_activities.filtered(
            lambda a: a.date_deadline == EXPECTED_DATE
            and EXPECTED_SUMMARY.lower() in (a.summary or "").lower()
        )
        act = match[:1] or call_activities[:1]
        act = act[0]

        if act.date_deadline != EXPECTED_DATE:
            failures.append(
                f"Activity due date is {act.date_deadline}, expected {EXPECTED_DATE}"
            )
        summary = act.summary or ""
        if EXPECTED_SUMMARY.lower() not in summary.lower():
            failures.append(
                f"Activity summary is '{summary}', "
                f"expected to contain '{EXPECTED_SUMMARY}'"
            )

    return failures
