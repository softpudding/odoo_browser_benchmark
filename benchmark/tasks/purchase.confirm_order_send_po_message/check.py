"""Postcondition checks for purchase.confirm_order_send_po_message."""

from datetime import date
import re


VENDOR_NAME = "Sterling Components"
TARGET_REF = "MED-SEND-PO-01"
DISTRACTOR_REF = "MED-SEND-PO-02"
TARGET_SUBJECT = "Sterling components order follow-up"
TARGET_BODY = (
    "Please review the confirmed purchase order and reply with the delivery date today."
)


def check(env):
    failures = []

    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        return [f"Vendor '{VENDOR_NAME}' not found"]

    po = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("partner_ref", "=", TARGET_REF),
    ], limit=1)
    if not po:
        return [f"RFQ '{TARGET_REF}' not found"]

    if po.state != "purchase":
        failures.append(f"Purchase order state is '{po.state}', expected 'purchase'")

    messages = env["mail.message"].search(
        [
            ("model", "=", "purchase.order"),
            ("res_id", "=", po.id),
            ("subject", "=", TARGET_SUBJECT),
        ],
        order="id desc",
    )
    if not messages:
        failures.append("No sent PO email found with the expected subject")
    else:
        msg = messages[0]
        body = re.sub(r"\s+", " ", (msg.body or "").lower())
        expected_body = re.sub(r"\s+", " ", TARGET_BODY.lower())
        if expected_body not in body:
            failures.append("Sent PO message body does not contain the expected text")

    distractor = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("partner_ref", "=", DISTRACTOR_REF),
    ], limit=1)
    if not distractor:
        failures.append(f"Distractor RFQ '{DISTRACTOR_REF}' not found")
    else:
        if distractor.state != "draft":
            failures.append(
                f"Distractor RFQ state is '{distractor.state}', expected 'draft'"
            )
        if env["mail.message"].search_count([
            ("model", "=", "purchase.order"),
            ("res_id", "=", distractor.id),
            ("subject", "=", TARGET_SUBJECT),
        ]):
            failures.append("Distractor RFQ received the custom send message")

    return failures
