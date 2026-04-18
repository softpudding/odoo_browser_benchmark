"""Postcondition checks for hr_holidays.bulk_approve_two_pending_requests.

Validates:
1. Eve Pending's leave ("Family vacation") is in state 'validate'.
2. Frank Pending's leave ("Wedding attendance") is in state 'validate'.
3. Alice Pending's leave ("Personal errands") is STILL in state 'confirm'.
4. The already-approved distractor is still 'validate'.
5. The already-refused distractor is still 'refuse'.
6. No extra hr.leave records were created.
"""


NAME_EVE = "Family vacation"
NAME_FRANK = "Wedding attendance"
NAME_ALICE = "Personal errands"
NAME_DONE = "Already approved holiday"
NAME_REFUSED = "Already refused day"

ALL_NAMES = [NAME_EVE, NAME_FRANK, NAME_ALICE, NAME_DONE, NAME_REFUSED]


def _find_one(env, name):
    recs = env["hr.leave"].with_context(active_test=False).search([
        ("name", "=", name),
    ])
    return recs


def check(env):
    failures = []

    eve = _find_one(env, NAME_EVE)
    frank = _find_one(env, NAME_FRANK)
    alice = _find_one(env, NAME_ALICE)
    done = _find_one(env, NAME_DONE)
    refused = _find_one(env, NAME_REFUSED)

    for label, rs in [
        ("Eve Pending", eve),
        ("Frank Pending", frank),
        ("Alice Pending", alice),
        ("Already approved", done),
        ("Already refused", refused),
    ]:
        if not rs:
            failures.append(f"{label}: leave record is missing")
        elif len(rs) > 1:
            failures.append(f"{label}: found {len(rs)} records, expected 1")

    if eve and eve[0].state != "validate":
        failures.append(
            f"Eve's leave state is '{eve[0].state}', expected 'validate'"
        )
    if frank and frank[0].state != "validate":
        failures.append(
            f"Frank's leave state is '{frank[0].state}', expected 'validate'"
        )
    if alice and alice[0].state != "confirm":
        failures.append(
            f"Alice's leave state is '{alice[0].state}', expected 'confirm' "
            f"(the task forbids approving her request)"
        )
    if done and done[0].state != "validate":
        failures.append(
            f"Distractor approved leave state is '{done[0].state}', expected 'validate'"
        )
    if refused and refused[0].state != "refuse":
        failures.append(
            f"Distractor refused leave state is '{refused[0].state}', expected 'refuse'"
        )

    # No extra hr.leave records created under our canonical names.
    all_recs = env["hr.leave"].with_context(active_test=False).search([
        ("name", "in", ALL_NAMES),
    ])
    if len(all_recs) != len(ALL_NAMES):
        failures.append(
            f"Expected {len(ALL_NAMES)} canonical leave records, found {len(all_recs)}"
        )

    return failures
