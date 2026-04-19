"""Postcondition checks for mass_mailing.create_mailing_select_list_schedule_send.

Validates:
1. Exactly one mailing.mailing with subject 'Spring Promo' exists.
2. state='in_queue' (not draft, not done/sending — agent used Schedule, not Send).
3. schedule_type='scheduled'.
4. schedule_date corresponds to May 20, 2026 10:00 in the user's timezone
   (stored as UTC in the DB).
5. mailing_model_name='mailing.list' and contact_list_ids includes the seeded
   'Bench Newsletter Subs' list.
6. body_html contains 'Save 20%' (agent typed into the iframe body editor).
7. The seeded mailing list is untouched.
"""

from datetime import datetime

import pytz


SUBJECT = "Spring Promo"
LIST_NAME = "Bench Newsletter Subs"


def check(env):
    failures = []

    mailings = env["mailing.mailing"].search([("subject", "=", SUBJECT)])
    if not mailings:
        return [f"Mailing with subject {SUBJECT!r} not found"]
    if len(mailings) > 1:
        failures.append(
            f"Found {len(mailings)} mailings named {SUBJECT!r}, expected exactly 1"
        )
    mailing = mailings[0]

    # --- state: Schedule (not Send, not draft save) ---
    if mailing.state != "in_queue":
        failures.append(
            f"Mailing state is {mailing.state!r}, expected 'in_queue' "
            "(agent must click Schedule, not Send / Save as draft)"
        )

    # --- schedule_type: scheduled (confirmed Schedule wizard) ---
    if mailing.schedule_type != "scheduled":
        failures.append(
            f"Mailing schedule_type is {mailing.schedule_type!r}, expected 'scheduled' "
            "(the Schedule dialog must be confirmed — not Send Now)"
        )

    # --- schedule_date: 2026-05-20 10:00 in the admin's timezone ---
    if not mailing.schedule_date:
        failures.append("Mailing schedule_date is not set (Schedule dialog skipped?)")
    else:
        # schedule_date is stored in UTC. The agent types "05/20/2026 10:00:00"
        # in the user's local timezone; Odoo converts to UTC on write.
        # Accept the value if it equals 2026-05-20 10:00 in either the admin's
        # configured tz OR UTC (covers envs where tz is blank/UTC).
        sd_utc_naive = mailing.schedule_date.replace(tzinfo=None)
        expected_local = datetime(2026, 5, 20, 10, 0, 0)

        user_tz_name = env.user.tz or "UTC"
        try:
            user_tz = pytz.timezone(user_tz_name)
        except pytz.UnknownTimeZoneError:
            user_tz = pytz.UTC

        # Convert stored UTC datetime into the user's local tz and compare.
        sd_utc = pytz.UTC.localize(sd_utc_naive)
        sd_user_local = sd_utc.astimezone(user_tz).replace(tzinfo=None)

        ok = (sd_user_local == expected_local) or (sd_utc_naive == expected_local)
        if not ok:
            failures.append(
                f"Mailing schedule_date is {sd_utc_naive} UTC "
                f"(= {sd_user_local} in {user_tz_name}), "
                f"expected {expected_local} local time (= user-TZ-adjusted UTC)"
            )

    # --- Recipients stays on Mailing List ---
    if mailing.mailing_model_name != "mailing.list":
        failures.append(
            f"mailing_model_name is {mailing.mailing_model_name!r}, expected 'mailing.list' "
            "(Recipients must remain 'Mailing List')"
        )

    # --- contact_list_ids includes seeded list ---
    list_names = mailing.contact_list_ids.mapped("name")
    if LIST_NAME not in list_names:
        failures.append(
            f"Mailing contact_list_ids = {list_names!r}, "
            f"expected to include {LIST_NAME!r}"
        )

    # --- body contains 'Save 20%' ---
    body = (mailing.body_html or "") + (getattr(mailing, "body_arch", "") or "")
    if "Save 20%" not in body:
        failures.append(
            "Mailing body_html/body_arch does not contain 'Save 20%' "
            "(the agent must type into the WYSIWYG body editor)"
        )

    # --- Seeded list untouched ---
    lst = env["mailing.list"].search([("name", "=", LIST_NAME)], limit=1)
    if not lst:
        failures.append(f"Seeded mailing list {LIST_NAME!r} is missing (do not delete it)")
    else:
        member_count = env["mailing.contact"].search_count([
            ("list_ids", "in", [lst.id]),
        ])
        if member_count != 3:
            failures.append(
                f"Seeded mailing list has {member_count} contacts, expected 3 "
                "(do not alter seeded list members)"
            )

    # --- Do-not-send invariants: sent_date must NOT be set (agent must not have sent) ---
    if mailing.sent_date:
        failures.append(
            f"Mailing sent_date={mailing.sent_date} — agent sent the mailing; "
            "task requires Schedule (in_queue) not Send (sending/done)"
        )

    return failures
