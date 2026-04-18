"""Postcondition checks for contacts.merge_three_duplicates_keep_email."""


DUP_NAME = "John Doe"
MASTER_EMAIL = "john@x.com"
MASTER_PHONE = "555-1234"
DECOY_REF = "BENCH-JD-DECOY"
ACME_REF = "BENCH-JD-ACME"
DUP_REFS = ["BENCH-JD-01", "BENCH-JD-02", "BENCH-JD-03"]


def check(env):
    failures = []
    Partner = env["res.partner"].with_context(active_test=False)

    # Decoy must still exist, be active, and untouched
    decoy = Partner.search([("ref", "=", DECOY_REF)], limit=1)
    if not decoy:
        failures.append(
            f"Distractor John Doe (ref {DECOY_REF}) is missing — it must "
            "NOT be merged or deleted"
        )
    else:
        if not decoy.active:
            failures.append(
                f"Distractor John Doe (ref {DECOY_REF}) was archived; it "
                "should be untouched and active"
            )
        if decoy.email != "jdoe@acme.com":
            failures.append(
                f"Distractor John Doe (ref {DECOY_REF}) email changed from "
                f"'jdoe@acme.com' to '{decoy.email}'"
            )
        if decoy.name != DUP_NAME:
            failures.append(
                f"Distractor John Doe (ref {DECOY_REF}) name changed to "
                f"'{decoy.name}'"
            )
        if not decoy.parent_id or decoy.parent_id.ref != ACME_REF:
            failures.append(
                f"Distractor John Doe (ref {DECOY_REF}) parent_id changed "
                f"from Acme Corp"
            )

    # Acme Corp must still be there and active
    acme = Partner.search([("ref", "=", ACME_REF)], limit=1)
    if not acme:
        failures.append(f"Acme Corp (ref {ACME_REF}) is missing")
    elif not acme.active:
        failures.append(f"Acme Corp (ref {ACME_REF}) was archived")

    # Exactly ONE of the three duplicate refs should remain — BENCH-JD-02,
    # because the prompt specifies the email-bearing record as master.
    survivors = Partner.search([("ref", "in", DUP_REFS)])
    if len(survivors) == 0:
        failures.append(
            "All three duplicate John Doe records are gone. Merge collapses "
            "into the master; BENCH-JD-02 should remain (email-bearing)."
        )
    elif len(survivors) > 1:
        failures.append(
            f"Expected exactly 1 surviving duplicate John Doe; found "
            f"{len(survivors)} with refs {survivors.mapped('ref')}"
        )
    elif survivors.ref != "BENCH-JD-02":
        failures.append(
            f"Surviving duplicate has ref '{survivors.ref}' but the master "
            "should be BENCH-JD-02 (the record with email john@x.com). This "
            "means the wrong record was picked as Destination Contact."
        )

    # The surviving John Doe (whichever ref) should carry the combined
    # email + phone from the merge.
    # Exclude decoy from the lookup.
    name_matches = Partner.search([
        ("name", "=", DUP_NAME),
        ("id", "!=", decoy.id if decoy else 0),
    ])
    if len(name_matches) == 0:
        failures.append(
            "No non-decoy 'John Doe' record found after merge — merge "
            "probably failed or unlinked the wrong record"
        )
    elif len(name_matches) > 1:
        failures.append(
            f"Expected exactly 1 non-decoy 'John Doe' record after merge; "
            f"found {len(name_matches)} with refs {name_matches.mapped('ref')}"
        )
    else:
        survivor = name_matches
        if not survivor.active:
            failures.append(
                f"Merged 'John Doe' record (ref {survivor.ref}) is archived; "
                "it should be active"
            )
        if survivor.email != MASTER_EMAIL:
            failures.append(
                f"Merged 'John Doe' (ref {survivor.ref}) should have email "
                f"'{MASTER_EMAIL}'; found '{survivor.email}'. The merge did "
                "not preserve the email field from the email-bearing source."
            )
        # Phone comparison — strip spaces for tolerance
        actual_phone = (survivor.phone or "").replace(" ", "")
        if actual_phone != MASTER_PHONE.replace(" ", ""):
            failures.append(
                f"Merged 'John Doe' (ref {survivor.ref}) should have phone "
                f"'{MASTER_PHONE}'; found '{survivor.phone}'. The merge did "
                "not preserve the phone field from the phone-bearing source."
            )

    return failures
