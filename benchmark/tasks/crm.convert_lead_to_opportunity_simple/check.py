"""Postcondition checks for crm.convert_lead_to_opportunity_simple.

Validates:
1. Lead "Spark Innovations - Pager SaaS" has been converted (type =
   'opportunity').
2. It is linked to the existing partner "Spark Innovations".
3. It is moved to the Qualified stage.
4. It has one exact Call activity scheduled.
5. The distractor lead is untouched (still type='lead').
6. No extra leads/opportunities were created with our seed names.
"""

from datetime import date


def check(env):
    failures = []

    partner = env["res.partner"].search(
        [("name", "=", "Spark Innovations")], limit=1
    )
    if not partner:
        return ["Customer 'Spark Innovations' not found"]

    lead = env["crm.lead"].search(
        [("name", "=", "Spark Innovations - Pager SaaS")], limit=1
    )
    if not lead:
        return ["Target lead 'Spark Innovations - Pager SaaS' not found"]

    if lead.type != "opportunity":
        failures.append(
            f"Lead type is '{lead.type}', expected 'opportunity'"
        )

    if not lead.partner_id or lead.partner_id.id != partner.id:
        partner_name = lead.partner_id.display_name if lead.partner_id else None
        failures.append(
            f"Linked partner is '{partner_name}', expected 'Spark Innovations'"
        )

    if not lead.stage_id or lead.stage_id.name != "Qualified":
        stage_name = lead.stage_id.name if lead.stage_id else None
        failures.append(
            f"Stage is '{stage_name}', expected 'Qualified'"
        )

    activities = env["mail.activity"].search([
        ("res_model", "=", "crm.lead"),
        ("res_id", "=", lead.id),
        ("summary", "=", "Confirm rollout timeline"),
    ])
    if len(activities) != 1:
        failures.append(
            f"Expected exactly 1 matching activity, found {len(activities)}"
        )
    else:
        activity = activities[0]
        if activity.activity_type_id.name != "Call":
            failures.append(
                f"Activity type is '{activity.activity_type_id.name}', expected 'Call'"
            )
        if activity.date_deadline != date(2026, 5, 15):
            failures.append(
                f"Activity due date is {activity.date_deadline}, expected 2026-05-15"
            )

    # Distractor lead untouched
    distractor = env["crm.lead"].search(
        [("name", "=", "Riverstone Retail - Fitting Line")], limit=1
    )
    if not distractor:
        failures.append("Distractor lead 'Riverstone Retail - Fitting Line' missing")
    elif distractor.type != "lead":
        failures.append(
            f"Distractor was changed — type is '{distractor.type}', expected 'lead'"
        )

    # No duplicate records with the same lead name
    all_target = env["crm.lead"].search(
        [("name", "=", "Spark Innovations - Pager SaaS")]
    )
    if len(all_target) != 1:
        failures.append(
            f"Expected exactly 1 record named 'Spark Innovations - Pager SaaS', "
            f"found {len(all_target)}"
        )

    return failures
