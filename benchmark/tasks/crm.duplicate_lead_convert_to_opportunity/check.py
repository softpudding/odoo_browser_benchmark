"""Postcondition checks for crm.duplicate_lead_convert_to_opportunity."""

TEMPLATE_LEAD_NAME = "Bench Template Lead"
CLONED_LEAD_NAME = "Bench Cloned Opp"
NEW_PARTNER_NAME = "Bench Cloned Customer"


def check(env):
    failures = []

    # --- Original template lead must still exist as type='lead' ---
    templates = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", TEMPLATE_LEAD_NAME),
    ])
    if len(templates) != 1:
        failures.append(
            f"Expected exactly 1 lead named '{TEMPLATE_LEAD_NAME}', found "
            f"{len(templates)}"
        )
    else:
        tmpl = templates[0]
        if tmpl.type != "lead":
            failures.append(
                f"Original '{TEMPLATE_LEAD_NAME}' has type='{tmpl.type}', "
                f"expected 'lead' (original must not be converted)"
            )
        if not tmpl.active:
            failures.append(f"Original '{TEMPLATE_LEAD_NAME}' was archived")

    # --- Cloned opportunity ---
    clones = env["crm.lead"].search([("name", "=", CLONED_LEAD_NAME)])
    if len(clones) != 1:
        failures.append(
            f"Expected exactly 1 record named '{CLONED_LEAD_NAME}', found "
            f"{len(clones)}"
        )
        return failures

    clone = clones[0]
    if clone.type != "opportunity":
        failures.append(
            f"Clone '{CLONED_LEAD_NAME}' has type='{clone.type}', "
            f"expected 'opportunity' (must be converted)"
        )
    if not clone.partner_id:
        failures.append(
            f"Clone '{CLONED_LEAD_NAME}' has no partner_id set, expected "
            f"a customer"
        )
    else:
        if clone.partner_id.name != NEW_PARTNER_NAME:
            failures.append(
                f"Clone '{CLONED_LEAD_NAME}' partner is "
                f"'{clone.partner_id.name}', expected '{NEW_PARTNER_NAME}'"
            )

    # Guard: no stray (copy) leftover
    leftovers = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", "Bench Template Lead (copy)"),
    ])
    if leftovers:
        failures.append(
            "A lead named 'Bench Template Lead (copy)' still exists — the "
            "duplicated lead must be renamed to 'Bench Cloned Opp'"
        )

    return failures
