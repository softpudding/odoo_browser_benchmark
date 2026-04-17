"""Postcondition checks for contacts.merge_duplicate_contacts."""


DUP_NAME = "Globex Corporation"
MASTER_VAT = "BE0477472701"
DISTRACTOR_SPECS = [
    {"name": "Globex plc", "email": "info@globex-plc.co.uk", "vat": "GB123456789"},
    {"name": "Globex Labs", "email": "research@globex-labs.io"},
]


def check(env):
    failures = []
    Partner = env["res.partner"].with_context(active_test=False)

    # Exactly one Globex Corporation should remain (merged master)
    survivors = Partner.search([("name", "=", DUP_NAME)])
    if len(survivors) == 0:
        return [
            f"No '{DUP_NAME}' record found after merge; the merge likely "
            "failed or all records were deleted"
        ]
    if len(survivors) > 1:
        failures.append(
            f"Expected exactly 1 '{DUP_NAME}' record after merge; found "
            f"{len(survivors)} (IDs: {survivors.ids})"
        )
        # Still check the most-complete one's VAT
        survivor = survivors.sorted(lambda p: (bool(p.vat), p.id))[-1]
    else:
        survivor = survivors

    # Master must keep its VAT
    if survivor.vat != MASTER_VAT:
        failures.append(
            f"Merged '{DUP_NAME}' should retain VAT '{MASTER_VAT}' (the "
            f"master record's VAT); found '{survivor.vat}'"
        )

    # Archive check: active surviving company, not archived
    if not survivor.active:
        failures.append(
            f"Merged '{DUP_NAME}' record is archived; it should be active"
        )

    # Distractors must be untouched and active
    for spec in DISTRACTOR_SPECS:
        rec = Partner.search([("name", "=", spec["name"])], limit=1)
        if not rec:
            failures.append(
                f"Distractor company '{spec['name']}' is missing — it should "
                "NOT have been merged or deleted"
            )
            continue
        if not rec.active:
            failures.append(
                f"Distractor '{spec['name']}' was archived; it should be "
                "untouched"
            )
        if spec.get("email") and rec.email != spec["email"]:
            failures.append(
                f"Distractor '{spec['name']}' email changed from "
                f"'{spec['email']}' to '{rec.email}'"
            )
        if spec.get("vat") and rec.vat != spec["vat"]:
            failures.append(
                f"Distractor '{spec['name']}' VAT changed from "
                f"'{spec['vat']}' to '{rec.vat}'"
            )

    return failures
