"""Clean up artifacts from previous runs."""


def cleanup(env):
    # Remove the bill first (tied by ref)
    bills = env["account.move"].search([
        ("ref", "=", "MSC-BILL-9921"),
        ("move_type", "=", "in_invoice"),
    ])
    for bill in bills:
        if bill.state == "posted":
            bill.button_draft()
        bill.unlink()

    # Then the source PO
    pos = env["purchase.order"].search(
        [("partner_ref", "=", "BENCH-BILL-PO")]
    )
    for po in pos:
        if po.state in ("purchase", "done"):
            po.button_cancel()
        po.unlink()
