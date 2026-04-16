"""Postcondition checks for sale.add_note_to_quotation.

Validates that:
1. An internal log note (subtype='Note') exists on quotation BENCH-NOTE-01
2. The note body contains the exact expected text
3. The quotation state remains 'draft'
"""


def check(env):
    failures = []

    # Find the target quotation
    so = env["sale.order"].search([
        ("client_order_ref", "=", "BENCH-NOTE-01"),
    ], limit=1)

    if not so:
        return ["Quotation with reference 'BENCH-NOTE-01' not found"]

    # Find log notes on this quotation
    messages = env["mail.message"].search([
        ("model", "=", "sale.order"),
        ("res_id", "=", so.id),
        ("subtype_id.name", "=", "Note"),
    ])

    if not messages:
        return ["No log note found on quotation 'BENCH-NOTE-01'"]

    # Check for the exact note text
    expected_text = "Customer requested delivery by May 1, 2026. Please coordinate with warehouse."
    found = False
    for msg in messages:
        if msg.body and expected_text in msg.body:
            found = True
            break

    if not found:
        note_bodies = [m.body[:100] for m in messages if m.body]
        failures.append(
            f"No log note with text '{expected_text}' found. "
            f"Found notes: {note_bodies}"
        )

    # Check quotation state remains draft
    if so.state != "draft":
        failures.append(
            f"Quotation state is '{so.state}', expected 'draft'"
        )

    return failures