"""Check repair.create_repair_order_add_fee_quotation_confirm."""

def check(env):
    failures = []
    repairs = env["repair.order"].search([("partner_id.name", "=", "Repair Harbor")], order="id desc", limit=1)
    if not repairs:
        return ["Repair order not found"]
    repair = repairs[0]
    if not repair.sale_order_id:
        failures.append("No linked quotation created")
        return failures
    if repair.sale_order_id.state != "sale":
        failures.append(f"Sale order state is {repair.sale_order_id.state!r}, expected 'sale'")
    if repair.state == "done":
        failures.append("Repair should not be completed")
    fee_lines = repair.sale_order_id.order_line.filtered(lambda l: l.product_id.display_name == "Bench Diagnostic Fee")
    if len(fee_lines) != 1:
        failures.append(f"Expected one fee line on quotation, found {len(fee_lines)}")
    elif abs(fee_lines[0].product_uom_qty - 1.0) > 0.0001:
        failures.append(f"Fee line qty is {fee_lines[0].product_uom_qty}, expected 1.0")
    invoices = repair.sale_order_id.invoice_ids.filtered(lambda inv: inv.move_type == "out_invoice")
    if invoices:
        failures.append("No invoice should be created")
    return failures
