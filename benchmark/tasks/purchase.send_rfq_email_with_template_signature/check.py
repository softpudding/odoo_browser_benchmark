"""Postcondition checks for purchase.send_rfq_email_with_template_signature.

Validates:
  - Target RFQ state flipped to 'sent' (but not 'purchase' — agent must
    NOT confirm).
  - A mail.message posted against the target RFQ contains BOTH:
      * the 'Purchase: Purchase Order' template marker
        ("Here is in attachment a purchase order") — proves the agent
        switched templates, AND
      * the appended sentence 'Please confirm by Friday.'.
    AND it must NOT still carry the 'Purchase: Request For Quotation'
    marker ("Here is in attachment a request for quotation") — catches
    agents that never switched templates.
  - Distractor RFQ is untouched (still 'draft', no outgoing email posted).
"""

import re


VENDOR_NAME = "Beacon Electrical Ltd."
TARGET_REF = "R-BENCH-EMAIL-001"
DISTRACTOR_REF = "R-BENCH-EMAIL-002"
APPEND_TEXT = "Please confirm by Friday"  # match without trailing period

# Marker from the REQUIRED template (Purchase: Purchase Order).
PO_TEMPLATE_MARKER = "here is in attachment a purchase order"
# Marker from the DEFAULT template (Purchase: Request For Quotation) — if
# this is still present in the sent body, the agent failed to switch.
RFQ_TEMPLATE_MARKER = "here is in attachment a request for quotation"


def _norm(s):
    return re.sub(r"\s+", " ", (s or "")).lower()


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
        return [f"Target RFQ '{TARGET_REF}' not found"]

    if po.state == "purchase":
        failures.append(
            "Target RFQ state is 'purchase' — agent must NOT confirm the order"
        )
    elif po.state != "sent":
        failures.append(
            f"Target RFQ state is '{po.state}', expected 'sent' (RFQ Sent)"
        )

    # Find the mail.message carrying the appended sentence on this PO.
    messages = env["mail.message"].search([
        ("model", "=", "purchase.order"),
        ("res_id", "=", po.id),
    ], order="id desc")

    appended_norm = _norm(APPEND_TEXT)

    match = None
    for msg in messages:
        body_norm = _norm(msg.body)
        if appended_norm in body_norm:
            match = msg
            if PO_TEMPLATE_MARKER in body_norm:
                break  # ideal: appended + switched template
    if match is None:
        failures.append(
            f"No mail.message on the target RFQ contains '{APPEND_TEXT}.'"
        )
    else:
        body_norm = _norm(match.body)
        if PO_TEMPLATE_MARKER not in body_norm:
            failures.append(
                "The sent email body is missing the 'Purchase: Purchase "
                "Order' template content — agent did not switch templates."
            )
        if RFQ_TEMPLATE_MARKER in body_norm:
            failures.append(
                "The sent email body still contains the default "
                "'Purchase: Request For Quotation' template text — agent "
                "did not switch to 'Purchase: Purchase Order'."
            )

    # Vendor / lines must be unchanged.
    if po.partner_id != vendor:
        failures.append("Target RFQ vendor was modified")

    lines = po.order_line.sorted("id")
    if len(lines) != 2:
        failures.append(
            f"Target RFQ has {len(lines)} lines, expected 2 unchanged"
        )
    else:
        expected = [
            ("Industrial Cable 10m", 5, 32.0),
            ("Relay Module", 10, 18.5),
        ]
        for i, (name, qty, price) in enumerate(expected):
            ln = lines[i]
            if ln.product_id.name != name:
                failures.append(
                    f"Line {i + 1} product is '{ln.product_id.name}', "
                    f"expected '{name}'"
                )
            if abs(ln.product_qty - qty) > 1e-6:
                failures.append(
                    f"Line {i + 1} qty is {ln.product_qty}, expected {qty}"
                )
            if abs(ln.price_unit - price) > 1e-6:
                failures.append(
                    f"Line {i + 1} price is {ln.price_unit}, expected {price}"
                )

    # Distractor must stay untouched.
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
        outgoing = env["mail.message"].search_count([
            ("model", "=", "purchase.order"),
            ("res_id", "=", distractor.id),
            ("message_type", "=", "email_outgoing"),
        ])
        if outgoing:
            failures.append(
                "Distractor RFQ unexpectedly received an outgoing email"
            )

    return failures
