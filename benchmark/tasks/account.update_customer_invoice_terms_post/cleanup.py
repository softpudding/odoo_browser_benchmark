"""Clean up artifacts from previous runs."""


def cleanup(env):
    invoices = env["account.move"].search([
        ("move_type", "=", "out_invoice"),
        "|",
        ("ref", "in", ["MED-CINV-01", "MED-CINV-02", "BRIGHT-READY"]),
        ("invoice_origin", "in", ["MED-CINV-01", "MED-CINV-02"]),
    ])
    for invoice in invoices:
        if invoice.state == "posted":
            invoice.button_draft()
        invoice.unlink()
