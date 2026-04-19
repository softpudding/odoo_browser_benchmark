"""Postcondition checks for crm.log_opportunity_note_internal.

Gates on:
  1. Exactly one 'Bench Note Opp' opportunity exists.
  2. A mail.message on that lead with:
       - message_type == 'comment'
       - subtype_id == ref('mail.mt_note')   (Log note, NOT Send message)
       - body (HTML-stripped) contains the substring 'demo' (case-insensitive)
"""

import re


OPP_NAME = "Bench Note Opp"
BODY_SUBSTRING = "demo"


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

    leads = env["crm.lead"].with_context(active_test=False).search([
        ("name", "=", OPP_NAME),
        ("type", "=", "opportunity"),
    ])
    if not leads:
        return [f"Opportunity '{OPP_NAME}' not found"]
    if len(leads) > 1:
        failures.append(
            f"Expected exactly 1 opportunity '{OPP_NAME}', found {len(leads)}"
        )
    lead = leads[0]
    if not lead.active:
        failures.append(f"Opportunity '{OPP_NAME}' is archived")

    mt_note = env.ref("mail.mt_note", raise_if_not_found=False)
    mt_comment = env.ref("mail.mt_comment", raise_if_not_found=False)
    if not mt_note:
        failures.append("mail.mt_note subtype is not registered in this DB")
        return failures

    messages = env["mail.message"].search([
        ("model", "=", "crm.lead"),
        ("res_id", "=", lead.id),
        ("message_type", "=", "comment"),
    ], order="id DESC")

    matching_note = []
    matching_comment = []
    matching_other = []
    for msg in messages:
        body = _strip_html(msg.body or "")
        if BODY_SUBSTRING.lower() not in body.lower():
            continue
        if msg.subtype_id.id == mt_note.id:
            matching_note.append(msg)
        elif mt_comment and msg.subtype_id.id == mt_comment.id:
            matching_comment.append(msg)
        else:
            matching_other.append(msg)

    if not matching_note:
        if matching_comment:
            failures.append(
                f"Found a chatter post containing '{BODY_SUBSTRING}' but "
                f"its subtype_id is 'mail.mt_comment' (Send message). The "
                f"task requires subtype_id='mail.mt_note' (Log note)."
            )
            return failures
        if matching_other:
            subs = [m.subtype_id.display_name for m in matching_other]
            failures.append(
                f"Found a chatter post containing '{BODY_SUBSTRING}' but "
                f"with unexpected subtype(s): {subs}. Expected "
                f"subtype_id='mail.mt_note' (Log note)."
            )
            return failures
        bodies = [
            (m.message_type, m.subtype_id.display_name, _strip_html(m.body or "")[:60])
            for m in messages
        ]
        failures.append(
            f"No Log-note (mail.mt_note) message on opportunity '{OPP_NAME}' "
            f"with body containing '{BODY_SUBSTRING}' was found. Messages "
            f"present: {bodies}"
        )
        return failures

    return failures
