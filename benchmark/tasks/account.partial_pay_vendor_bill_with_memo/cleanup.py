"""Cleanup for account.partial_pay_vendor_bill_with_memo."""

TARGET_REF = "VB-PARTIAL-01"
DISTRACTOR_REF = "VB-PARTIAL-02"


def cleanup(env):
    bills = env["account.move"].search([
        ("move_type", "=", "in_invoice"),
        ("ref", "in", [TARGET_REF, DISTRACTOR_REF]),
    ])
    for bill in bills:
        for payment in bill._get_reconciled_payments():
            if payment.state == "posted":
                payment.action_draft()
            payment.unlink()
        if bill.state == "posted":
            bill.button_draft()
        if bill.state == "draft":
            bill.button_cancel()
        bill.unlink()

    env["account.payment"].search([("memo", "=", "PARTIAL-JUN-600")]).unlink()
