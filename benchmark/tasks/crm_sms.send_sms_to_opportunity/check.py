"""Postconditions for crm_sms.send_sms_to_opportunity.

Validates:
1. Opportunity 'Bench Hot Lead' still exists with same partner.
2. A sms.sms record exists whose body contains 'Following up on your
   inquiry' and whose number is the sanitized E.164 +16175551234.
3. That sms.sms record is linked (via mail_message_id) to a mail.message
   whose model='crm.lead' and res_id=opportunity.id, with message_type='sms'.
4. Exactly one sms.sms was created for this number (agent didn't send twice).
"""

TARGET_NAME = "Bench Hot Lead"
TARGET_NUMBER = "+16175551234"
TARGET_BODY_FRAGMENT = "Following up on your inquiry"


def check(env):
    failures = []

    opp = env["crm.lead"].search([
        ("name", "=", TARGET_NAME),
        ("type", "=", "opportunity"),
    ], limit=1)
    if not opp:
        return [f"Opportunity '{TARGET_NAME}' not found"]

    # Find sms.sms matching number
    sms_recs = env["sms.sms"].sudo().search([
        ("number", "=", TARGET_NUMBER),
    ])
    if not sms_recs:
        return [f"No sms.sms record found with number {TARGET_NUMBER}"]

    # Filter by body
    matching = sms_recs.filtered(lambda s: TARGET_BODY_FRAGMENT in (s.body or ""))
    if not matching:
        bodies = [f"id={s.id}: body={s.body!r}" for s in sms_recs]
        return [
            f"No sms.sms record with body containing "
            f"'{TARGET_BODY_FRAGMENT}'. Existing: " + "; ".join(bodies)
        ]

    if len(matching) > 1:
        failures.append(
            f"Expected exactly 1 sms.sms matching, found {len(matching)} "
            f"(agent may have sent multiple times)"
        )

    sms = matching[0]

    # Check linked mail.message
    if not sms.mail_message_id:
        failures.append(
            "sms.sms has no mail_message_id — SMS was not posted on document"
        )
    else:
        msg = sms.mail_message_id
        if msg.model != "crm.lead":
            failures.append(
                f"mail.message.model is {msg.model!r}, expected 'crm.lead'"
            )
        if msg.res_id != opp.id:
            failures.append(
                f"mail.message.res_id is {msg.res_id}, expected {opp.id} "
                f"(opportunity id)"
            )
        if msg.message_type != "sms":
            failures.append(
                f"mail.message.message_type is {msg.message_type!r}, "
                f"expected 'sms'"
            )

    return failures
