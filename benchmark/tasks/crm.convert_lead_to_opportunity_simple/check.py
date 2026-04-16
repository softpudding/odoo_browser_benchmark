"""Postcondition checks for crm.convert_lead_to_opportunity_simple.

Validates:
1. Lead "Spark Innovations - Pager SaaS" has been converted (type =
   'opportunity').
2. It is linked to the existing partner "Spark Innovations".
3. The distractor lead is untouched (still type='lead').
4. No extra leads/opportunities were created with our seed names.
"""


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
