"""Postcondition checks for repair.cancel_repair_log_internal_reason."""


REPAIR_REF = "RO/CANCEL/0001"
EXPECTED_NOTE = "Customer requested cancellation - replacement parts no longer needed"


def check(env):
    failures = []

    repairs = env["repair.order"].search([("name", "=", REPAIR_REF)])
    if not repairs:
        return [f"Repair order '{REPAIR_REF}' is missing"]
    if len(repairs) != 1:
        return [f"Expected exactly 1 repair order '{REPAIR_REF}', found {len(repairs)}"]

    repair = repairs[0]
    if repair.state != "cancel":
        failures.append(
            f"Repair order state is '{repair.state}', expected 'cancel' "
            f"(agent did not click 'Cancel Repair')"
        )

    note_subtype = env.ref("mail.mt_note", raise_if_not_found=False)
    messages = repair.message_ids
    matching_notes = messages.filtered(
        lambda m: (
            EXPECTED_NOTE in (m.body or "")
            and (note_subtype is None or m.subtype_id.id == note_subtype.id)
        )
    )
    if not matching_notes:
        any_with_text = messages.filtered(lambda m: EXPECTED_NOTE in (m.body or ""))
        if any_with_text:
            failures.append(
                "A chatter message with the expected text exists, but it is "
                "not an internal Note (likely a public 'Send message' instead "
                "of 'Log note')"
            )
        else:
            failures.append(
                f"No internal note with the exact text '{EXPECTED_NOTE}' was "
                f"found in the chatter of {REPAIR_REF}"
            )
    elif len(matching_notes) > 1:
        failures.append(
            f"Found {len(matching_notes)} internal notes with the expected text — "
            f"agent posted the same note multiple times"
        )

    return failures
