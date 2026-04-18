"""Postcondition checks for sale_timesheet.log_timesheet_on_so_invoice_delivered."""

PARTNER_NAME = "Bench Services Co"
SERVICE_CODE = "SERV-BENCH-TS"
DISTRACTOR_CODE = "SERV-BENCH-MAN"
SO_REF = "S-BENCH-TS-001"


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
    if line.product_id.default_code != SERVICE_CODE:
        failures.append(
            f"SO line product is {line.product_id.default_code!r}, "
            f"expected {SERVICE_CODE!r}"
        )
    if abs(line.product_uom_qty - 10.0) > 1e-6:
        failures.append(
            f"SO line product_uom_qty is {line.product_uom_qty}, expected 10.0"
        )
    if abs(line.qty_delivered - 6.0) > 1e-6:
        failures.append(
            f"SO line qty_delivered is {line.qty_delivered}, expected 6.0"
        )

    # Project + task from auto-generation
    projects = order.project_ids
    if not projects:
        failures.append("No project linked to the SO (auto-generation failed?)")
        return failures
    project = projects[0]
    tasks = env["project.task"].search([("project_id", "=", project.id)])
    if len(tasks) != 1:
        failures.append(
            f"Expected exactly 1 task on the auto-generated project, found {len(tasks)}"
        )
        return failures
    task = tasks[0]

    # Timesheets: exactly 2 rows, totalling 6.0 hours, all admin.
    admin = env.ref("base.user_admin")
    admin_employee = env["hr.employee"].search([
        ("user_id", "=", admin.id),
    ], limit=1)

    timesheets = env["account.analytic.line"].search([
        ("task_id", "=", task.id),
    ])
    if len(timesheets) != 2:
        failures.append(
            f"Expected exactly 2 timesheet rows on the task, found {len(timesheets)} "
            f"({timesheets.mapped('name')!r})"
        )
    total_hours = sum(timesheets.mapped("unit_amount"))
    if abs(total_hours - 6.0) > 1e-6:
        failures.append(
            f"Timesheet total hours is {total_hours}, expected 6.0"
        )
    # Each timesheet employee should resolve to the admin-linked hr.employee
    # (or at least the name should contain 'admin'/'Administrator').
    if admin_employee:
        wrong_employee = timesheets.filtered(
            lambda t: t.employee_id and t.employee_id != admin_employee
        )
        if wrong_employee:
            failures.append(
                f"Some timesheet rows have a non-admin employee: "
                f"{wrong_employee.mapped('employee_id.name')!r}"
            )
    # Each row should be >0 hours (non-empty)
    zero_rows = timesheets.filtered(lambda t: t.unit_amount <= 0)
    if zero_rows:
        failures.append(
            f"{len(zero_rows)} timesheet row(s) have zero/negative hours"
        )

    # Invoice side: exactly one draft out_invoice for partner.
    invoices = env["account.move"].search([
        ("partner_id", "=", partner.id),
        ("move_type", "=", "out_invoice"),
    ])
    if len(invoices) != 1:
        failures.append(
            f"Expected exactly 1 customer invoice for {PARTNER_NAME!r}, "
            f"found {len(invoices)} (states={invoices.mapped('state')!r})"
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
    if inv_line.product_id.default_code != SERVICE_CODE:
        failures.append(
            f"Invoice line product is {inv_line.product_id.default_code!r}, "
            f"expected {SERVICE_CODE!r}"
        )
    if abs(inv_line.quantity - 6.0) > 1e-6:
        failures.append(
            f"Invoice line quantity is {inv_line.quantity}, expected 6.0"
        )
    if abs(inv_line.price_unit - 150.0) > 1e-6:
        failures.append(
            f"Invoice line price_unit is {inv_line.price_unit}, expected 150.0"
        )
    if abs(inv_line.price_subtotal - 900.0) > 1e-6:
        failures.append(
            f"Invoice line price_subtotal is {inv_line.price_subtotal}, expected 900.0"
        )

    # Invoice must reference the SO (invoice_origin or linked invoice line
    # sale_line_ids). sale.advance.payment.inv sets invoice_origin = SO.name.
    if invoice.invoice_origin != order.name:
        failures.append(
            f"Invoice invoice_origin is {invoice.invoice_origin!r}, "
            f"expected {order.name!r}"
        )

    # Distractor product must NOT be on the invoice.
    distractor = env["product.product"].search(
        [("default_code", "=", DISTRACTOR_CODE)], limit=1
    )
    if distractor and distractor in inv_lines.mapped("product_id"):
        failures.append(
            f"Distractor product {DISTRACTOR_CODE!r} should not appear on the invoice"
        )

    return failures
