"""Postcondition checks for purchase.cancel_rfq_log_note."""

NOTE_TEXT = "Vendor asked us to pause this request until next quarter."


def check(env):
    failures = []

    target = env["purchase.order"].search([("name", "=", "P-RFQ-CANCEL-01")], limit=1)
    if not target:
        return ["Target RFQ 'P-RFQ-CANCEL-01' not found"]

    if target.state != "cancel":
        failures.append(f"Target RFQ state is '{target.state}', expected 'cancel'")

    note = env["mail.message"].search([
        ("model", "=", "purchase.order"),
        ("res_id", "=", target.id),
    ], order="id desc")
    if not any(NOTE_TEXT in (msg.body or "") for msg in note):
        failures.append("Expected internal note not found on target RFQ")

    distractor = env["purchase.order"].search([("name", "=", "P-RFQ-CANCEL-02")], limit=1)
    if not distractor:
        failures.append("Distractor RFQ 'P-RFQ-CANCEL-02' not found")
    elif distractor.state != "draft":
        failures.append(f"Distractor RFQ state is '{distractor.state}', expected 'draft'")

    return failures
