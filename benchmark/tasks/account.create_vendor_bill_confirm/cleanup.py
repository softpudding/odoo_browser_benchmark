"""Clean up artifacts from previous runs."""


def cleanup(env):
    bills = env["account.move"].search([
        ("ref", "=", "MSC-INV-4421"),
        ("move_type", "=", "in_invoice"),
    ])
    for bill in bills:
        if bill.state == "posted":
            bill.button_draft()
        bill.unlink()
