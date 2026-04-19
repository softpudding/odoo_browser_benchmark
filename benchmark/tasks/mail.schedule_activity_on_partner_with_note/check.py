"""Postcondition checks for mail.schedule_activity_on_partner_with_note.

Gates on:
  1. Exactly one 'Bench Activity Partner' contact exists.
  2. Exactly one mail.activity row on that partner with:
       - res_model == 'res.partner'
       - res_id == partner.id
       - activity_type_id.name == 'To-Do'
       - summary == 'Follow up call'
       - date_deadline == 2026-05-15
       - note (HTML) contains the substring 'Q2 plan' once stripped of
         <p>/<br> tags.
"""

import re
from datetime import date


PARTNER_NAME = "Bench Activity Partner"
EXPECTED_SUMMARY = "Follow up call"
EXPECTED_DEADLINE = date(2026, 5, 15)
EXPECTED_NOTE_SUBSTR = "Q2 plan"


def _strip_html(html: str) -> str:
    text = re.sub(r"<[^>]+>", "", html or "")
    text = (text
            .replace("&nbsp;", " ")
            .replace("&amp;", "&")
            .replace("&#39;", "'")
            .replace("&quot;", '"'))
    return " ".join(text.split()).strip()


def check(env):
    failures = []

    partners = env["res.partner"].with_context(active_test=False).search([
        ("name", "=", PARTNER_NAME),
    ])
    if len(partners) == 0:
        return [f"Partner '{PARTNER_NAME}' not found"]
    if len(partners) > 1:
        failures.append(
            f"Expected exactly 1 partner named '{PARTNER_NAME}', "
            f"found {len(partners)}"
        )
    partner = partners[0]
    if not partner.active:
        failures.append(f"Partner '{PARTNER_NAME}' is archived")

    activities = env["mail.activity"].search([
        ("res_model", "=", "res.partner"),
        ("res_id", "=", partner.id),
    ])
    if not activities:
        return failures + [
            f"No mail.activity row found on partner '{PARTNER_NAME}' "
            f"(res_model='res.partner', res_id={partner.id}). The agent "
            f"likely did not click Schedule in the wizard, or the wizard "
            f"was cancelled."
        ]
    if len(activities) > 1:
        failures.append(
            f"Expected exactly 1 mail.activity on '{PARTNER_NAME}', "
            f"found {len(activities)} (summaries: "
            f"{activities.mapped('summary')})"
        )

    # Match by summary first; if that fails, explain what we saw.
    matching = activities.filtered(lambda a: (a.summary or "") == EXPECTED_SUMMARY)
    if not matching:
        failures.append(
            f"No mail.activity with summary=={EXPECTED_SUMMARY!r} on "
            f"'{PARTNER_NAME}'. Summaries present: "
            f"{activities.mapped('summary')}"
        )
        return failures

    activity = matching[0]

    # activity_type: enforce the default 'To-Do'.
    atype_name = (activity.activity_type_id.name or "").strip()
    if atype_name != "To-Do":
        failures.append(
            f"Activity type is {atype_name!r}, expected 'To-Do'"
        )

    # date_deadline: must exactly equal 2026-05-15.
    if activity.date_deadline != EXPECTED_DEADLINE:
        failures.append(
            f"Activity date_deadline is {activity.date_deadline}, "
            f"expected {EXPECTED_DEADLINE}"
        )

    # note: HTML field — strip tags and check for the expected substring.
    note_text = _strip_html(activity.note or "")
    if EXPECTED_NOTE_SUBSTR.lower() not in note_text.lower():
        failures.append(
            f"Activity note does not contain {EXPECTED_NOTE_SUBSTR!r}. "
            f"Note text (stripped) was: {note_text!r}"
        )

    return failures
