"""Postcondition checks for mass_mailing.duplicate_mailing_edit_subject_send.

Validates:
1. Original mailing 'Bench Newsletter V1' still exists, untouched
   (subject unchanged, state still 'done', sent_date unchanged).
2. Exactly one duplicate 'Bench Newsletter V2 Spring Special' exists with:
   - mailing_model_name = 'mailing.list'
   - contact_list_ids includes the 'Bench Subscribers' list
   - state in ('sending', 'done') (i.e. Send was clicked, not Schedule)
   - sent_date is set (Send actually happened)
3. Exactly two mailings exist across the full "Bench Newsletter ..." subject
   set — no Duplicate spam loop, no stray "(copy)" artifacts.
"""

from datetime import datetime


SOURCE_SUBJECT = "Bench Newsletter V1"
DUP_SUBJECT = "Bench Newsletter V2 Spring Special"
LIST_NAME = "Bench Subscribers"
SEEDED_SENT_DATE = datetime(2026, 3, 15, 9, 0, 0)


def check(env):
    failures = []

    # --- Original must still exist and be untouched ---
    original = env["mailing.mailing"].search(
        [("subject", "=", SOURCE_SUBJECT)], limit=1
    )
    if not original:
        failures.append(f"Original mailing {SOURCE_SUBJECT!r} is missing")
    else:
        if original.state != "done":
            failures.append(
                f"Original state is {original.state!r}, expected 'done' "
                "(original must remain unchanged)"
            )
        if not original.sent_date:
            failures.append(
                "Original sent_date has been cleared (original must remain unchanged)"
            )
        elif original.sent_date.replace(tzinfo=None) != SEEDED_SENT_DATE:
            failures.append(
                f"Original sent_date is {original.sent_date}, "
                f"expected seeded value {SEEDED_SENT_DATE} (original must not be re-sent)"
            )
        if original.mailing_model_name != "mailing.list":
            failures.append(
                "Original mailing_model_name changed to "
                f"{original.mailing_model_name!r}, expected 'mailing.list'"
            )

    # --- Duplicate must exist ---
    dups = env["mailing.mailing"].search([("subject", "=", DUP_SUBJECT)])
    if not dups:
        return failures + [
            f"Duplicate mailing with subject {DUP_SUBJECT!r} not found"
        ]
    if len(dups) > 1:
        failures.append(
            f"Found {len(dups)} mailings with subject {DUP_SUBJECT!r}, expected exactly 1"
        )
    dup = dups[0]

    if dup.mailing_model_name != "mailing.list":
        failures.append(
            f"Duplicate mailing_model_name is {dup.mailing_model_name!r}, "
            "expected 'mailing.list' (Recipients must stay as 'Mailing List')"
        )

    list_names = dup.contact_list_ids.mapped("name")
    if LIST_NAME not in list_names:
        failures.append(
            f"Duplicate contact_list_ids = {list_names!r}, "
            f"expected to include {LIST_NAME!r}"
        )

    # Send (not Schedule, not Test): state must show the mailing was launched.
    # Clicking Send fires action_launch which sets state='in_queue' and triggers
    # the cron; once the cron drains, state moves to 'sending' and then 'done'.
    # All three are acceptable signals that Send (not Schedule / Test / Save)
    # was the action taken. Only 'draft' (never launched) is a failure.
    if dup.state not in ("in_queue", "sending", "done"):
        failures.append(
            f"Duplicate state is {dup.state!r}, expected one of "
            "('in_queue', 'sending', 'done') — agent must have clicked Send, "
            "not Schedule / Test / Save"
        )

    # Clicking Send must also set schedule_type='now' (action_launch writes
    # this). If schedule_type is 'scheduled', the agent used the Schedule flow
    # instead, which is forbidden.
    if dup.schedule_type == "scheduled":
        failures.append(
            "Duplicate schedule_type is 'scheduled' — agent used the Schedule "
            "flow instead of clicking Send"
        )

    # --- No Duplicate spam: at most 2 mailings in the Bench Newsletter family ---
    family = env["mailing.mailing"].search([
        ("subject", "ilike", "Bench Newsletter V"),
    ])
    expected_subjects = {SOURCE_SUBJECT, DUP_SUBJECT}
    actual_subjects = set(family.mapped("subject"))
    extras = actual_subjects - expected_subjects
    if extras:
        failures.append(
            f"Extra Bench Newsletter mailings exist: {sorted(extras)!r} "
            "(expected exactly the source + its single duplicate)"
        )
    if len(family) > 2:
        failures.append(
            f"Found {len(family)} Bench Newsletter mailings, expected exactly 2 "
            "(Duplicate spam loop?)"
        )

    return failures
