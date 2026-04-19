"""Cleanup for account.create_vendor_bill_from_scratch_pay."""

VENDOR_NAME = "Bench Bill Vendor"
TARGET_REF = "BENCH-VBILL-001"


def cleanup(env):
    vendor = env["res.partner"].search(
        [("name", "=", VENDOR_NAME)], limit=1
    )

    # Drop all payments for this vendor first (including reconciled ones).
    if vendor:
        pays = env["account.payment"].search([
            ("partner_id", "=", vendor.id),
        ])
        for pay in pays:
            pmove = pay.move_id
            if pmove:
                for line in pmove.line_ids.filtered(
                    lambda l: l.matched_debit_ids or l.matched_credit_ids
                ):
                    line.remove_move_reconcile()
            if pay.state == "posted":
                try:
                    pay.action_draft()
                except Exception:
                    pass
            try:
                pay.action_cancel()
            except Exception:
                pass
            try:
                pay.unlink()
            except Exception:
                pass

    # Drop the target bill (any state) and any orphan bills for this vendor.
    bills = env["account.move"].search([
        ("ref", "=", TARGET_REF),
        ("move_type", "=", "in_invoice"),
    ])
    for bill in bills:
        for line in bill.line_ids.filtered(
            lambda l: l.matched_debit_ids or l.matched_credit_ids
        ):
            line.remove_move_reconcile()
        if bill.state == "posted":
            bill.button_draft()
        if bill.state == "draft":
            bill.button_cancel()
        bill.unlink()

    if vendor:
        orphans = env["account.move"].search([
            ("partner_id", "=", vendor.id),
            ("move_type", "in", ["in_invoice", "in_refund"]),
        ])
        for o in orphans:
            for line in o.line_ids.filtered(
                lambda l: l.matched_debit_ids or l.matched_credit_ids
            ):
                line.remove_move_reconcile()
            if o.state == "posted":
                o.button_draft()
            if o.state == "draft":
                o.button_cancel()
            o.unlink()
