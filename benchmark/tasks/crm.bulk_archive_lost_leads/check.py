"""Postcondition checks for crm.bulk_archive_lost_leads.

Validates:
1. The three target Bench Lost leads still exist and have active=False.
2. The distractor Bench Keep 4 still exists and has active=True.
3. No seeded lead was deleted.
"""


TARGET_NAMES = ["Bench Lost 1", "Bench Lost 2", "Bench Lost 3"]
DISTRACTOR_NAME = "Bench Keep 4"


def check(env):
    failures = []
    Lead = env["crm.lead"].with_context(active_test=False)

    for name in TARGET_NAMES:
        leads = Lead.search([("name", "=", name)])
        if len(leads) == 0:
            failures.append(
                f"Target lead '{name}' is missing — it must not be deleted. "
                "Use Archive (cog Actions > Archive), not Delete/Unlink."
            )
            continue
        if len(leads) > 1:
            failures.append(
                f"Expected exactly 1 lead named '{name}'; found {len(leads)}"
            )
            continue
        lead = leads[0]
        if lead.active:
            failures.append(
                f"Target lead '{name}' still has active=True; expected "
                "active=False after bulk Archive."
            )

    distractors = Lead.search([("name", "=", DISTRACTOR_NAME)])
    if len(distractors) == 0:
        failures.append(
            f"Distractor lead '{DISTRACTOR_NAME}' is missing — it must stay "
            "in the database, untouched."
        )
    else:
        for d in distractors:
            if not d.active:
                failures.append(
                    f"Distractor lead '{DISTRACTOR_NAME}' was archived "
                    "(active=False); it must remain active=True."
                )

    # Record-count guard: the four seeded leads must all still exist.
    seeded = Lead.search([("name", "in", TARGET_NAMES + [DISTRACTOR_NAME])])
    if len(seeded) != 4:
        failures.append(
            f"Expected 4 seeded Bench leads; found {len(seeded)}"
        )

    return failures
