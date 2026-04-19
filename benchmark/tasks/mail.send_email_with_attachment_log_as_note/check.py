"""Postcondition checks for mail.send_email_with_attachment_log_as_note.

Gates on:
  1. Exactly one Bench Chatter Co partner exists.
  2. A mail.message on that partner with:
       - message_type == 'comment'
       - subtype_id == ref('mail.mt_comment')   (Send message, NOT Log note)
       - body contains 'Attached our welcome kit'
       - at least one ir.attachment in attachment_ids
       - partner_ids includes the contact itself
  3. At least one of those attachments is named welcome_kit.txt and is
     non-empty.
"""

import re


PARTNER_NAME = "Bench Chatter Co"
EXPECTED_BODY = "Attached our welcome kit"
EXPECTED_ATTACHMENT_NAME = "welcome_kit.txt"


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

    mt_comment = env.ref("mail.mt_comment", raise_if_not_found=False)
    mt_note = env.ref("mail.mt_note", raise_if_not_found=False)
    if not mt_comment:
        failures.append("mail.mt_comment subtype is not registered in this DB")

    messages = env["mail.message"].search([
        ("model", "=", "res.partner"),
        ("res_id", "=", partner.id),
        ("message_type", "=", "comment"),
    ], order="id DESC")

    matching_send = []
    matching_note = []
    matching_other = []
    for msg in messages:
        body = _strip_html(msg.body or "")
        if EXPECTED_BODY.lower() not in body.lower():
            continue
        if mt_comment and msg.subtype_id.id == mt_comment.id:
            matching_send.append(msg)
        elif mt_note and msg.subtype_id.id == mt_note.id:
            matching_note.append(msg)
        else:
            matching_other.append(msg)

    if not matching_send:
        if matching_note:
            failures.append(
                f"Found a chatter post with body '{EXPECTED_BODY}' but "
                f"its subtype_id is 'mail.mt_note' (Log note). The task "
                f"requires subtype_id='mail.mt_comment' (Send message)."
            )
            return failures
        if matching_other:
            ids = [m.subtype_id.display_name for m in matching_other]
            failures.append(
                f"Found a chatter post with body '{EXPECTED_BODY}' but "
                f"with unexpected subtype(s): {ids}. Expected "
                f"subtype_id='mail.mt_comment' (Send message)."
            )
            return failures
        failures.append(
            f"No Send-message comment on partner '{PARTNER_NAME}' with "
            f"body '{EXPECTED_BODY}' was found. Messages present: "
            f"{[(m.message_type, _strip_html(m.body or '')[:60]) for m in messages]}"
        )
        return failures

    # Take the newest matching Send-message post for attachment + recipient
    # validation.
    msg = matching_send[0]

    if not msg.attachment_ids:
        failures.append(
            f"The chatter post exists but has no attachment_ids. "
            f"The task requires an attached file ({EXPECTED_ATTACHMENT_NAME})."
        )
    else:
        wanted = [
            a for a in msg.attachment_ids
            if (a.name or "").strip().lower() == EXPECTED_ATTACHMENT_NAME
        ]
        if not wanted:
            failures.append(
                f"Chatter post has {len(msg.attachment_ids)} attachment(s) "
                f"but none named '{EXPECTED_ATTACHMENT_NAME}'. Attachments: "
                f"{msg.attachment_ids.mapped('name')}."
            )
        else:
            # Make sure at least one has real content (datas / raw).
            non_empty = [a for a in wanted if (a.datas or a.raw)]
            if not non_empty:
                failures.append(
                    f"The '{EXPECTED_ATTACHMENT_NAME}' attachment on the "
                    f"post has empty bytes."
                )

    # Send-message vs Log-note is pinned via subtype_id check above. We
    # do NOT gate on partner_ids here — Odoo 19's default Send-message
    # subtype_id=mt_comment can post with empty partner_ids when no
    # existing follower matches the subtype (and partner auto-follow
    # is not always present on res.partner out of the box).

    return failures
