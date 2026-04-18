"""Postcondition checks for sale_purchase.mto_so_generate_po_change_vendor_confirm."""


VENDOR_A = "Atlas Components"
VENDOR_B = "Beacon Components"
PRODUCT_NAME = "Bench Relay Module"
SO_REF = "MTO-VENDOR-SWITCH"
QTY = 3.0
PRICE_B = 62.0


def check(env):
    failures = []

    so = env["sale.order"].search([("client_order_ref", "=", SO_REF)], limit=1)
    if not so:
        return [f"Sales order '{SO_REF}' not found"]
    if so.state != "sale":
        failures.append(f"Sale order state is {so.state!r}, expected 'sale'")

    line = so.order_line.filtered(lambda l: l.product_id.name == PRODUCT_NAME)[:1]
    if not line:
        failures.append(f"Sale order line for {PRODUCT_NAME!r} not found")
    else:
        line = line[0]
        if abs(line.product_uom_qty - QTY) > 0.0001:
            failures.append(f"Sale order quantity is {line.product_uom_qty}, expected {QTY}")

    pos = env["purchase.order"].with_context(active_test=False).search([
        ("origin", "=", so.name),
    ])
    if len(pos) != 1:
        failures.append(
            f"Expected exactly 1 generated purchase order for origin {so.name!r}, found {len(pos)}"
        )
        return failures

    po = pos[0]
    if po.partner_id.name != VENDOR_B:
        failures.append(
            f"Purchase order vendor is {po.partner_id.name!r}, expected {VENDOR_B!r}"
        )
    if po.state != "purchase":
        failures.append(f"Purchase order state is {po.state!r}, expected 'purchase'")

    po_lines = po.order_line.filtered(lambda l: l.product_id.name == PRODUCT_NAME)
    if len(po_lines) != 1:
        failures.append(
            f"Expected exactly 1 purchase line for {PRODUCT_NAME!r}, found {len(po_lines)}"
        )
    else:
        po_line = po_lines[0]
        if abs(po_line.product_qty - QTY) > 0.0001:
            failures.append(
                f"Purchase quantity is {po_line.product_qty}, expected {QTY}"
            )
        if abs(po_line.price_unit - PRICE_B) > 0.01:
            failures.append(
                f"Purchase unit price is {po_line.price_unit}, expected {PRICE_B}"
            )

    atlas = env["res.partner"].search([("name", "=", VENDOR_A)], limit=1)
    if atlas:
        atlas_pos = env["purchase.order"].with_context(active_test=False).search([
            ("origin", "=", so.name),
            ("partner_id", "=", atlas.id),
        ])
        if atlas_pos:
            failures.append("A generated RFQ for Atlas Components still exists")

    return failures
