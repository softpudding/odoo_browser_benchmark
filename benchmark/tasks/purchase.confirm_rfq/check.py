"""Postcondition checks for purchase.confirm_rfq."""

PRODUCT_NAME = "Precision Fastener Set"


def check(env):
    failures = []

    vendor = env["res.partner"].search([("name", "=", "Nimbus Industrial Supply")], limit=1)
    if not vendor:
        return ["Vendor 'Nimbus Industrial Supply' not found"]

    po = env["purchase.order"].search([
        ("partner_id", "=", vendor.id),
        ("origin", "=", "BENCH-CONFIRM-01"),
    ], limit=1)
    if not po:
        return ["RFQ for 'Nimbus Industrial Supply' with source 'BENCH-CONFIRM-01' not found"]

    if po.state != "purchase":
        failures.append(
            f"Purchase Order state is {po.state!r}, expected 'purchase'"
        )

    if len(po.order_line) != 1:
        failures.append(f"Expected 1 order line, found {len(po.order_line)}")
        return failures

    line = po.order_line[0]
    if line.product_id.name != PRODUCT_NAME:
        failures.append(
            f"Order line product is {line.product_id.name!r}, expected {PRODUCT_NAME!r}"
        )
    if line.product_qty != 6:
        failures.append(f"Order quantity is {line.product_qty!r}, expected 6")
    if line.price_unit != 24.0:
        failures.append(f"Unit price is {line.price_unit!r}, expected 24.0")

    return failures
