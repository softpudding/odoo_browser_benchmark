"""Postcondition checks for account.send_invoice_with_extra_recipient."""

import re


TARGET_REF = "SEND-APR-17"
DISTRACTOR_REF = "SEND-APR-18"
TARGET_SUBJECT = "Beacon Offshore invoice review"
TARGET_BODY = (
    "Please review the April service invoice and reply with any approval notes by Friday."
)
REQUIRED_RECIPIENTS = {
    "finance@beacon-offshore.example.com",
    "controller@beacon-offshore.example.com",
}


def check(env):
    failures = []

    target = env["account.move"].search([("ref", "=", TARGET_REF)], limit=1)
    distractor = env["account.move"].search([("ref", "=", DISTRACTOR_REF)], limit=1)

    if not target:
        return [f"Target invoice {TARGET_REF!r} not found"]
    if not distractor:
        return [f"Distractor invoice {DISTRACTOR_REF!r} not found"]

    if target.state != "posted":
        failures.append(f"Target invoice state is {target.state!r}, expected 'posted'")
    if not target.is_move_sent:
        failures.append("Target invoice was not marked as sent")

    messages = env["mail.message"].search(
        [
            ("model", "=", "account.move"),
            ("res_id", "=", target.id),
            ("subject", "=", TARGET_SUBJECT),
        ],
        order="id desc",
    )
    if not messages:
        failures.append("No sent invoice email message found with the expected subject")
    else:
        msg = messages[0]
        body = re.sub(r"\s+", " ", (msg.body or "").lower())
        expected_body = re.sub(r"\s+", " ", TARGET_BODY.lower())
        if expected_body not in body:
            failures.append("Sent invoice message body does not contain the expected text")
        recipient_emails = {email for email in msg.partner_ids.mapped("email") if email}
        missing = REQUIRED_RECIPIENTS - recipient_emails
        if missing:
            failures.append(
                f"Sent invoice recipients missing expected email(s): {sorted(missing)}"
            )
        if "finance@beacon-onshore.example.com" in recipient_emails:
            failures.append("Distractor recipient was included on the sent target invoice")

    if distractor.is_move_sent:
        failures.append("Distractor invoice was marked sent")

    distractor_msgs = env["mail.message"].search_count(
        [
            ("model", "=", "account.move"),
            ("res_id", "=", distractor.id),
            ("subject", "=", TARGET_SUBJECT),
        ]
    )
    if distractor_msgs:
        failures.append("Distractor invoice received the custom send message")

    return failures
