"""Postcondition checks for hr_expense.split_submitted_report_resubmit.

Validates the batch split outcome:
- Meal (40.00) and Taxi (25.00) must end up in 'approved' state.
- Gadget (500.00) must end up in 'refused' state.
- The Gadget expense chatter must contain the refusal reason 'Not compliant'.
- No expense may be deleted (all 3 still exist).
- No Gadget expense amount should have been modified.
"""

MEAL_NAME = "R-BENCH-SPLIT-001 Meal"
GADGET_NAME = "R-BENCH-SPLIT-001 Gadget"
TAXI_NAME = "R-BENCH-SPLIT-001 Taxi"
EXPECTED_REASON = "Not compliant"


def check(env):
    failures = []

    def _fetch(name):
        recs = env["hr.expense"].search([("name", "=", name)])
        return recs

    meal = _fetch(MEAL_NAME)
    gadget = _fetch(GADGET_NAME)
    taxi = _fetch(TAXI_NAME)

    if not meal:
        failures.append(f"No expense named {MEAL_NAME!r} — agent may have deleted it")
    if not gadget:
        failures.append(f"No expense named {GADGET_NAME!r} — agent may have deleted it")
    if not taxi:
        failures.append(f"No expense named {TAXI_NAME!r} — agent may have deleted it")

    if len(meal) > 1:
        failures.append(f"Found {len(meal)} expenses named {MEAL_NAME!r}; expected exactly 1")
    if len(gadget) > 1:
        failures.append(f"Found {len(gadget)} expenses named {GADGET_NAME!r}; expected exactly 1")
    if len(taxi) > 1:
        failures.append(f"Found {len(taxi)} expenses named {TAXI_NAME!r}; expected exactly 1")

    # Early exit if any record is missing — the rest of the checks require them.
    if not meal or not gadget or not taxi:
        return failures

    meal = meal[0]
    gadget = gadget[0]
    taxi = taxi[0]

    if meal.state != "approved":
        failures.append(
            f"Meal state is {meal.state!r}, expected 'approved' (approval_state={meal.approval_state!r})"
        )
    if taxi.state != "approved":
        failures.append(
            f"Taxi state is {taxi.state!r}, expected 'approved' (approval_state={taxi.approval_state!r})"
        )
    if gadget.state != "refused":
        failures.append(
            f"Gadget state is {gadget.state!r}, expected 'refused' (approval_state={gadget.approval_state!r})"
        )

    # Reason must appear somewhere on the gadget chatter.
    messages = gadget.message_ids
    bodies = " ".join((m.body or "") for m in messages)
    if EXPECTED_REASON.lower() not in bodies.lower():
        failures.append(
            f"Expected refusal reason {EXPECTED_REASON!r} not found in Gadget chatter"
        )

    # Amounts must not have been altered.
    if abs(meal.total_amount_currency - 40.0) > 0.01:
        failures.append(f"Meal total_amount_currency is {meal.total_amount_currency}, expected 40.00")
    if abs(gadget.total_amount_currency - 500.0) > 0.01:
        failures.append(
            f"Gadget total_amount_currency is {gadget.total_amount_currency}, expected 500.00 "
            "— agent should not edit the amount when refusing"
        )
    if abs(taxi.total_amount_currency - 25.0) > 0.01:
        failures.append(f"Taxi total_amount_currency is {taxi.total_amount_currency}, expected 25.00")

    return failures
