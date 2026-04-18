"""Postcondition checks for crm.create_lead_from_email_alias_log_message."""

import re

TEAM_NAME = "Inbound"
TARGET_ALIAS = "leads-inbound"
TARGET_ALIAS_CONTACT = "partners"
LEAD_NAME = "Inbound Inquiry from Sample"
LEAD_EMAIL = "prospect@external.test"
CHATTER_MESSAGE = "Asked about Bench Pro pricing."
TARGET_PRIORITY = "1"   # Medium -> one filled star
TAG_NAME = "Website"


def _strip_html(html: str) -> str:
    text = re.sub(r"<[^>]+>", "", html or "")
    # Collapse whitespace and decode the common HTML entities that Odoo's
    # editor emits.
    text = (text
            .replace("&nbsp;", " ")
            .replace("&amp;", "&")
            .replace("&#39;", "'")
            .replace("&quot;", '"'))
    return " ".join(text.split()).strip()


def check(env):
    failures = []

    # --- Team alias ---
    team = env["crm.team"].with_context(active_test=False).search([
        ("name", "=", TEAM_NAME),
    ], limit=1)
    if not team:
        return [f"Sales Team '{TEAM_NAME}' not found"]
    if team.alias_name != TARGET_ALIAS:
        failures.append(
            f"Team '{TEAM_NAME}' alias_name is '{team.alias_name}', "
            f"expected '{TARGET_ALIAS}'"
        )
    if not team.alias_id:
        failures.append(f"Team '{TEAM_NAME}' has no alias record")
    elif team.alias_id.alias_contact != TARGET_ALIAS_CONTACT:
        failures.append(
            f"Team '{TEAM_NAME}' alias_contact is "
            f"'{team.alias_id.alias_contact}', expected "
            f"'{TARGET_ALIAS_CONTACT}' (Authenticated Partners)"
        )

    # --- Lead ---
    leads = env["crm.lead"].search([("name", "=", LEAD_NAME)])
    if len(leads) != 1:
        failures.append(
            f"Expected exactly 1 lead named '{LEAD_NAME}', found {len(leads)}"
        )
        return failures

    lead = leads[0]
    if lead.type != "lead":
        failures.append(
            f"Record type is '{lead.type}', expected 'lead' (not an opportunity)"
        )
    if (lead.email_from or "").strip().lower() != LEAD_EMAIL.lower():
        failures.append(
            f"Lead email_from is '{lead.email_from}', expected '{LEAD_EMAIL}'"
        )
    if lead.priority != TARGET_PRIORITY:
        failures.append(
            f"Lead priority is '{lead.priority}', expected "
            f"'{TARGET_PRIORITY}' (Medium = one star)"
        )
    tag_names = {t.name for t in lead.tag_ids}
    if TAG_NAME not in tag_names:
        failures.append(
            f"Lead tags are {sorted(tag_names)}, expected to include '{TAG_NAME}'"
        )

    # --- Chatter message (must be a regular comment, not an internal note) ---
    note_subtype = env.ref("mail.mt_note", raise_if_not_found=False)
    messages = env["mail.message"].search([
        ("model", "=", "crm.lead"),
        ("res_id", "=", lead.id),
        ("message_type", "=", "comment"),
    ])

    matching_regular = []
    matching_internal = []
    for msg in messages:
        body_text = _strip_html(msg.body or "")
        if CHATTER_MESSAGE not in body_text:
            continue
        is_internal = (
            msg.subtype_id == note_subtype if note_subtype else msg.is_internal
        )
        if is_internal:
            matching_internal.append(msg)
        else:
            matching_regular.append(msg)

    if not matching_regular:
        if matching_internal:
            failures.append(
                "The chatter entry was posted as an internal 'Log note' "
                "instead of as 'Send message' — it must be a regular message"
            )
        else:
            failures.append(
                f"No regular chatter message with body '{CHATTER_MESSAGE}' "
                f"was found on the lead"
            )

    # Distractor guard: the lead must not have been converted to an opportunity.
    if lead.type == "opportunity":
        failures.append("Lead was converted to an opportunity")

    return failures
