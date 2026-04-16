"""Clean up artifacts from previous runs."""


def cleanup(env):
    bills = env["account.move"].search([
        ("move_type", "=", "in_invoice"),
        ("ref", "in", ["MED-VB-DRAFT-01", "MED-VB-DRAFT-02", "MSC-8841"]),
    ])
    for bill in bills:
        if bill.state == "posted":
            bill.button_draft()
        bill.unlink()
