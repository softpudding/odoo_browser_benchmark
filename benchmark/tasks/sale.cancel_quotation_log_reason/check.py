"""Postcondition checks for sale.cancel_quotation_log_reason.

Validates:
1. BENCH-CANCEL-01 is in state 'cancel'.
2. A log-note message with the expected text is attached to it.
3. Both distractor quotations are still in 'draft'.
"""


EXPECTED_NOTE = (
    "Customer withdrew RFP. Cancelling to remove from active pipeline."
)


def check(env):
    failures = []

    target = env["sale.order"].search(
        [("client_order_ref", "=", "BENCH-CANCEL-01")], limit=1
    )
    if not target:
        return ["Target quotation 'BENCH-CANCEL-01' not found"]

    if target.state != "cancel":
        failures.append(
            f"Target state is '{target.state}', expected 'cancel'"
        )

    notes = env["mail.message"].search([
        ("model", "=", "sale.order"),
        ("res_id", "=", target.id),
        ("subtype_id.name", "=", "Note"),
    ])
    found = any(n.body and EXPECTED_NOTE in (n.body or "") for n in notes)
    if not found:
        bodies = [n.body[:120] for n in notes if n.body]
        failures.append(
            f"Log note with expected text not found. Notes: {bodies}"
        )

    for ref in ("BENCH-NOCANCEL-A", "BENCH-NOCANCEL-B"):
        other = env["sale.order"].search(
            [("client_order_ref", "=", ref)], limit=1
        )
        if not other:
            failures.append(f"Distractor '{ref}' is missing")
        elif other.state != "draft":
            failures.append(
                f"Distractor '{ref}' state is '{other.state}', expected 'draft'"
            )

    return failures
