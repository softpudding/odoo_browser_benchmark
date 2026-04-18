"""Cleanup for repair.create_repair_order_add_parts_complete_invoice."""


def cleanup(env):
    env["repair.order"].search([("name", "=", "RO/BENCH/0001")]).unlink()
    invoices = env["account.move"].search([("invoice_origin", "=", "RO/BENCH/0001")])
    for invoice in invoices:
        if invoice.state == "posted":
            invoice.button_draft()
        invoice.button_cancel()
    invoices.unlink()
    env["sale.order"].search([("origin", "=", "RO/BENCH/0001")]).unlink()
    env["product.template"].search([("name", "in", ["Bench Pump Core", "Bench Repair Seal"])]).unlink()
