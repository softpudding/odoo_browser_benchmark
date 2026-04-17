"""Postcondition checks for crm.mark_opportunity_won_update_revenue.

Validates:
1. Target opportunity is in a won stage (stage_id.is_won=True).
2. Target expected_revenue is 52000.
3. Target priority is medium (2 stars).
4. Two distractors are in their original stages with unchanged revenue.
"""


TARGET = "Crestline Networks - Managed VPN"
EXPECTED_REVENUE = 52000.0

DISTRACTORS = {
    # name -> (original stage name, original revenue)
    "Crestline Networks - Firewall Expansion": ("New", 25000.0),
    "Crestline Retail - POS Refresh": ("Proposition", 18000.0),
}


def check(env):
    failures = []
    Lead = env["crm.lead"].with_context(active_test=False)

    target = Lead.search([("name", "=", TARGET)], limit=1)
    if not target:
        return [f"Target opportunity '{TARGET}' not found"]

    if not target.stage_id or not target.stage_id.is_won:
        stage_name = target.stage_id.name if target.stage_id else "(none)"
        failures.append(
            f"Target stage is '{stage_name}' (is_won=False); expected a won stage"
        )

    if abs(target.expected_revenue - EXPECTED_REVENUE) > 0.01:
        failures.append(
            f"Target expected_revenue={target.expected_revenue}, "
            f"expected {EXPECTED_REVENUE}"
        )
    if target.priority != "2":
        failures.append(
            f"Target priority is '{target.priority}', expected '2'"
        )

    for name, (orig_stage, orig_rev) in DISTRACTORS.items():
        other = Lead.search([("name", "=", name)], limit=1)
        if not other:
            failures.append(f"Distractor opportunity '{name}' is missing")
            continue
        if not other.stage_id or other.stage_id.name != orig_stage:
            actual = other.stage_id.name if other.stage_id else "(none)"
            failures.append(
                f"Distractor '{name}' stage is '{actual}', expected '{orig_stage}'"
            )
        if abs(other.expected_revenue - orig_rev) > 0.01:
            failures.append(
                f"Distractor '{name}' expected_revenue={other.expected_revenue}, "
                f"expected {orig_rev}"
            )
        if other.priority not in (False, "0"):
            failures.append(
                f"Distractor '{name}' priority is '{other.priority}', expected default"
            )

    return failures
