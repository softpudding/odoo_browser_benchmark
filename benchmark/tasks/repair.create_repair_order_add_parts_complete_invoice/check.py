"""Postcondition checks for repair.create_repair_order_add_parts_complete_invoice."""


def check(env):
    failures = []

    repair = env["repair.order"].search([("name", "=", "RO/BENCH/0001")], limit=1)
    if not repair:
        return ["Repair order 'RO/BENCH/0001' not found"]

    if repair.state != "done":
        failures.append(f"Repair state is '{repair.state}', expected 'done'")
    if not repair.sale_order_id:
        failures.append("Repair order is not linked to a sale order")
        return failures

    part_lines = repair.move_ids.filtered(lambda move: move.product_id.display_name == "Bench Repair Seal")
    if len(part_lines) != 1:
        failures.append(f"Expected exactly 1 repair part line, found {len(part_lines)}")
    else:
        line = part_lines[0]
        if abs(line.product_uom_qty - 1.0) > 0.0001:
            failures.append(f"Repair part demand is {line.product_uom_qty}, expected 1.0")
        if abs(line.quantity - 1.0) > 0.0001:
            failures.append(f"Repair part consumed quantity is {line.quantity}, expected 1.0")

    invoices = repair.sale_order_id.invoice_ids.filtered(lambda inv: inv.move_type == "out_invoice")
    if len(invoices) != 1:
        failures.append(f"Expected exactly 1 customer invoice, found {len(invoices)}")
    else:
        invoice = invoices[0]
        if invoice.state != "posted":
            failures.append(f"Invoice state is '{invoice.state}', expected 'posted'")
        seal_lines = invoice.invoice_line_ids.filtered(lambda line: line.product_id.display_name == "Bench Repair Seal")
        if len(seal_lines) != 1:
            failures.append("Invoice does not contain the repair part line")

    return failures
