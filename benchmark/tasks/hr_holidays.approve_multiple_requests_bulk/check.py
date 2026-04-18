"""Postcondition checks for hr_holidays.approve_multiple_requests_bulk.

Validates:
1. Bench Alice/Bob/Carol's leaves are in state='validate' (approved).
2. Bench Diana's leave is still in state='refuse' (already-refused
   distractor; must NOT be re-approved).
3. No Alice/Bob/Carol leave was refused during the approval workflow.
4. No extra hr.leave records created with the canonical names.
"""


BENCH_CONFIRM_LEAVES = [
    "Bench Alice vacation",
    "Bench Bob vacation",
    "Bench Carol vacation",
]
DIANA_REFUSED_LEAVE = "Bench Diana vacation"
ALL_LEAVE_NAMES = BENCH_CONFIRM_LEAVES + [DIANA_REFUSED_LEAVE]


def _find_one(env, name):
    return env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", name),
    ])


def check(env):
    failures = []

    for name in BENCH_CONFIRM_LEAVES:
        recs = _find_one(env, name)
        if not recs:
            failures.append(f"{name}: leave record missing")
            continue
        if len(recs) > 1:
            failures.append(
                f"{name}: found {len(recs)} records, expected 1"
            )
            continue
        if recs[0].state != "validate":
            failures.append(
                f"{name}: state is '{recs[0].state}', expected 'validate' "
                f"(bulk approve should have moved it from confirm to validate)"
            )

    diana = _find_one(env, DIANA_REFUSED_LEAVE)
    if not diana:
        failures.append(f"{DIANA_REFUSED_LEAVE}: leave record missing")
    elif len(diana) > 1:
        failures.append(
            f"{DIANA_REFUSED_LEAVE}: found {len(diana)} records, expected 1"
        )
    elif diana[0].state != "refuse":
        failures.append(
            f"{DIANA_REFUSED_LEAVE}: state is '{diana[0].state}', "
            f"expected 'refuse' (Diana's already-refused request must "
            f"not be re-approved or modified)"
        )

    # No Alice/Bob/Carol leave may be in 'refuse' state at the end —
    # the agent should not have refused any pending request.
    bad_refused = env["hr.leave"].with_context(active_test=False).search([
        ("name", "in", BENCH_CONFIRM_LEAVES),
        ("state", "=", "refuse"),
    ])
    if bad_refused:
        failures.append(
            f"{len(bad_refused)} pending bench leave(s) were refused; "
            f"the task requires approval, not refusal"
        )

    # No extra hr.leave records with the canonical names.
    all_recs = env["hr.leave"].with_context(active_test=False).search([
        ("name", "in", ALL_LEAVE_NAMES),
    ])
    if len(all_recs) != len(ALL_LEAVE_NAMES):
        failures.append(
            f"Expected {len(ALL_LEAVE_NAMES)} canonical bench leaves, "
            f"found {len(all_recs)}"
        )

    return failures
