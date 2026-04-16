"""Postcondition checks for sale.set_commitment_date."""

from datetime import datetime


PARTNER_NAME = "Highfield Consulting"
TARGET_REF = "BENCH-COMMIT-01"
DISTRACTOR_REF = "BENCH-COMMIT-02"
EXPECTED_COMMITMENT_DATE = datetime(2026, 5, 20, 0, 0, 0)


def check(env):
    failures = []

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return [f"Partner '{PARTNER_NAME}' not found"]

    order = env["sale.order"].search([
        ("partner_id", "=", partner.id),
        ("client_order_ref", "=", TARGET_REF),
    ], limit=1)
    if not order:
        return [f"Sales order '{TARGET_REF}' not found"]

    if order.state != "sale":
        failures.append(
            f"Sales order state is '{order.state}', expected 'sale' (confirmed)"
        )

    if not order.commitment_date:
        failures.append("Delivery Date (commitment_date) was not set")
    elif order.commitment_date.date() != EXPECTED_COMMITMENT_DATE.date():
        failures.append(
            f"Delivery Date is {order.commitment_date.date()}, expected 2026-05-20"
        )

    if order.invoice_ids:
        failures.append("Target order was invoiced — should not be invoiced")

    # Distractor order must still be confirmed with no delivery date change
    distractor = env["sale.order"].search([
        ("partner_id", "=", partner.id),
        ("client_order_ref", "=", DISTRACTOR_REF),
    ], limit=1)
    if not distractor:
        failures.append(f"Distractor order '{DISTRACTOR_REF}' not found")
    else:
        if distractor.state not in ("sale", "done"):
            failures.append(
                f"Distractor order state is '{distractor.state}', expected 'sale'"
            )

    return failures
