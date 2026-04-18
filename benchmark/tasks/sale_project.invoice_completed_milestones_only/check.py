"""Postcondition checks for sale_project.invoice_completed_milestones_only."""

PARTNER_NAME = "Bench Quad Milestone Client"
PRODUCT_CODE = "SERV-BENCH-MS-Q"
SO_REF = "S-BENCH-MS-002"
REACHED_NAMES = {"M1 Setup", "M2 Build"}
UNREACHED_NAMES = {"M3 Test", "M4 Launch"}


def check(env):
    failures = []

    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        return [f"Partner '{PARTNER_NAME}' not found"]

    order = env["sale.order"].search([("client_order_ref", "=", SO_REF)], limit=1)
    if not order:
        return [f"Sales order '{SO_REF}' not found"]
    if order.state != "sale":
        failures.append(f"SO state is {order.state!r}, expected 'sale'")

    if len(order.order_line) != 1:
        failures.append(
            f"SO should have exactly 1 line, found {len(order.order_line)}"
        )
        return failures

    line = order.order_line[0]
    if abs(line.product_uom_qty - 4.0) > 1e-6:
        failures.append(
            f"SO line product_uom_qty is {line.product_uom_qty}, expected 4.0"
        )
    if abs(line.qty_delivered - 2.0) > 1e-6:
        failures.append(
            f"SO line qty_delivered is {line.qty_delivered}, expected 2.0"
        )

    project = order.project_ids[:1]
    if not project:
        failures.append("No project linked to the SO")
        return failures
    project = project[0]

    milestones = env["project.milestone"].search([
        ("project_id", "=", project.id),
        ("sale_line_id", "=", line.id),
    ])
    if len(milestones) != 4:
        failures.append(
            f"Expected exactly 4 milestones on project {project.name!r}, "
            f"found {len(milestones)}"
        )

    reached = milestones.filtered(lambda m: m.is_reached)
    reached_names = set(reached.mapped("name"))
    if reached_names != REACHED_NAMES:
        failures.append(
            f"Reached milestone names are {reached_names!r}, "
            f"expected {REACHED_NAMES!r}"
        )

    unreached = milestones.filtered(lambda m: not m.is_reached)
    unreached_names = set(unreached.mapped("name"))
    if unreached_names != UNREACHED_NAMES:
        failures.append(
            f"Unreached milestone names are {unreached_names!r}, "
            f"expected {UNREACHED_NAMES!r}"
        )

    invoices = env["account.move"].search([
        ("partner_id", "=", partner.id),
        ("move_type", "=", "out_invoice"),
    ])
    if len(invoices) != 1:
        failures.append(
            f"Expected exactly 1 customer invoice for {PARTNER_NAME!r}, "
            f"found {len(invoices)}"
        )
        return failures

    invoice = invoices[0]
    if invoice.state != "draft":
        failures.append(
            f"Invoice state is {invoice.state!r}, expected 'draft'"
        )

    inv_lines = invoice.invoice_line_ids.filtered(
        lambda l: l.display_type in (False, "product") and l.product_id
    )
    if len(inv_lines) != 1:
        failures.append(
            f"Expected exactly 1 product invoice line, found {len(inv_lines)} "
            f"({inv_lines.mapped('name')!r})"
        )
        return failures

    inv_line = inv_lines[0]
    if inv_line.product_id.default_code != PRODUCT_CODE:
        failures.append(
            f"Invoice line product is {inv_line.product_id.default_code!r}, "
            f"expected {PRODUCT_CODE!r}"
        )
    if abs(inv_line.quantity - 2.0) > 1e-6:
        failures.append(
            f"Invoice line quantity is {inv_line.quantity}, expected 2.0"
        )
    if abs(inv_line.price_unit - 500.0) > 1e-6:
        failures.append(
            f"Invoice line price_unit is {inv_line.price_unit}, expected 500.0"
        )
    if abs(inv_line.price_subtotal - 1000.0) > 1e-6:
        failures.append(
            f"Invoice line price_subtotal is {inv_line.price_subtotal}, "
            f"expected 1000.0"
        )

    return failures
