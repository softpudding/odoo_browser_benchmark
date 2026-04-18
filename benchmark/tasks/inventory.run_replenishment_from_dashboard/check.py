"""Postcondition checks for inventory.run_replenishment_from_dashboard."""

VENDOR_NAME = "Bench Supplies Ltd"
PRODUCT_NAME = "Bench Reorder Widget"
EXPECTED_QTY = 28.0
ORDERPOINT_MIN = 10.0
ORDERPOINT_MAX = 30.0


def check(env):
    failures = []

    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        return [f"Vendor '{VENDOR_NAME}' not found"]

    product = env["product.product"].search([("name", "=", PRODUCT_NAME)], limit=1)
    if not product:
        return [f"Product '{PRODUCT_NAME}' not found"]

    pos = env["purchase.order"].search([("partner_id", "=", vendor.id)])
    if not pos:
        failures.append(
            f"No purchase order created for vendor '{VENDOR_NAME}'."
        )
        return failures

    if len(pos) > 1:
        failures.append(
            f"Expected exactly 1 purchase order for vendor '{VENDOR_NAME}', "
            f"found {len(pos)}."
        )

    po = pos[0]
    if po.state != "draft":
        failures.append(
            f"Purchase order state is {po.state!r}, expected 'draft'."
        )

    product_lines = po.order_line.filtered(lambda l: l.product_id == product)
    if not product_lines:
        failures.append(
            f"Purchase order has no line for product '{PRODUCT_NAME}'."
        )
    else:
        if len(product_lines) > 1:
            failures.append(
                f"Expected 1 line for '{PRODUCT_NAME}', found {len(product_lines)}."
            )
        line = product_lines[0]
        # Allow rounding/uom variations: accept anything from 10 (min) up to
        # the system's max (30). Ideal: 28.
        if line.product_qty < ORDERPOINT_MIN or line.product_qty > ORDERPOINT_MAX:
            failures.append(
                f"Line product_qty is {line.product_qty}, expected near {EXPECTED_QTY} "
                f"(must be between {ORDERPOINT_MIN} and {ORDERPOINT_MAX})."
            )

    # Distractor check: no other POs created for other vendors mid-task.
    # (We only flag if extra POs reference our seeded product.)
    other_pos = env["purchase.order"].search([
        ("partner_id", "!=", vendor.id),
        ("order_line.product_id", "=", product.id),
    ])
    if other_pos:
        failures.append(
            f"Unexpected extra purchase order(s) referencing '{PRODUCT_NAME}': "
            f"{other_pos.mapped('name')}"
        )

    # Orderpoint state: Odoo's action_replenish will auto-delete a manual
    # orderpoint that was created by SUPERUSER once qty_to_order is satisfied.
    # We therefore allow either: (a) the orderpoint still exists with the seeded
    # min/max unchanged, or (b) the orderpoint is gone and qty_to_order is
    # consumed by the new PO. We only flag if it still exists with mutated
    # min/max — which would mean the agent edited the rule.
    op = env["stock.warehouse.orderpoint"].search([
        ("product_id", "=", product.id),
    ], limit=1)
    if op:
        if op.product_min_qty != ORDERPOINT_MIN:
            failures.append(
                f"Orderpoint min changed to {op.product_min_qty}, "
                f"expected {ORDERPOINT_MIN}."
            )
        if op.product_max_qty != ORDERPOINT_MAX:
            failures.append(
                f"Orderpoint max changed to {op.product_max_qty}, "
                f"expected {ORDERPOINT_MAX}."
            )

    return failures
