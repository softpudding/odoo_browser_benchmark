"""Seed vendor + product for account.create_vendor_bill_from_scratch_pay.

Category: deep_ui_interaction (HARD, tier 3).

Seeds ONLY a vendor partner and a consumable product. The agent must
create the vendor bill from scratch (no pre-existing draft bill exists),
fill the header with the exact vendor / date / reference / single line,
click Confirm to post, then click Pay in the header and click the
primary Create Payment button in the account.payment.register wizard
to register a full payment.

Three sequential gates stress three distinct failure modes in one task:

  1. Create-from-scratch with exact single line — agents commonly leave
     a phantom empty second line (Odoo auto-adds an empty row when the
     first line is edited). The prompt REQUIRES exactly one line.
  2. Post (Confirm) — a statusbar button flip.
  3. Pay (wizard) — accept defaults + click primary Create Payment. The
     wizard footer has both "Create Payment" (primary) and "Discard"
     (secondary); agents that click Discard or close the modal fail.

Defaults in the Register Payment wizard are correct for a full payment
on a single bill (Bank journal, today's date, full amount 150.00,
Manual method, auto-filled memo), so this task is intentionally an
"accept defaults + click primary" wizard — the difficulty is in the
three-step sequence and the create-from-scratch phantom-line trap, not
a non-default wizard choice.
"""

VENDOR_NAME = "Bench Bill Vendor"
PRODUCT_NAME = "Bench Bill Item"
TARGET_REF = "BENCH-VBILL-001"


def _cleanup_bill(env, ref):
    """Remove any prior-run bill and its reconciled payments.

    Posted payments with reconciled counterpart lines cannot be deleted
    directly; follow the unreconcile → action_draft → unlink order.
    """
    moves = env["account.move"].search([
        ("ref", "=", ref),
        ("move_type", "=", "in_invoice"),
    ])
    for mv in moves:
        # Drop any linked payments first (full or partial reconciles).
        for payment in mv._get_reconciled_payments():
            pmove = payment.move_id
            if pmove:
                for line in pmove.line_ids.filtered(
                    lambda l: l.matched_debit_ids or l.matched_credit_ids
                ):
                    line.remove_move_reconcile()
            if payment.state == "posted":
                try:
                    payment.action_draft()
                except Exception:
                    pass
            try:
                payment.action_cancel()
            except Exception:
                pass
            try:
                payment.unlink()
            except Exception:
                pass

        # Unreconcile any remaining receivable/payable lines on the bill.
        for line in mv.line_ids.filtered(
            lambda l: l.matched_debit_ids or l.matched_credit_ids
        ):
            line.remove_move_reconcile()
        if mv.state == "posted":
            mv.button_draft()
        if mv.state == "draft":
            mv.button_cancel()
        mv.unlink()


def setup(env):
    # --- 1. Cleanup prior runs ---
    _cleanup_bill(env, TARGET_REF)

    # Sweep any orphan bills/refunds/payments for this vendor.
    vendor = env["res.partner"].search(
        [("name", "=", VENDOR_NAME)], limit=1
    )
    if vendor:
        orphan_pays = env["account.payment"].search([
            ("partner_id", "=", vendor.id),
        ])
        for pay in orphan_pays:
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

        orphan_bills = env["account.move"].search([
            ("partner_id", "=", vendor.id),
            ("move_type", "in", ["in_invoice", "in_refund"]),
        ])
        for bill in orphan_bills:
            for line in bill.line_ids.filtered(
                lambda l: l.matched_debit_ids or l.matched_credit_ids
            ):
                line.remove_move_reconcile()
            if bill.state == "posted":
                bill.button_draft()
            if bill.state == "draft":
                bill.button_cancel()
            bill.unlink()

    # --- 2. Ensure vendor exists with supplier_rank=1 ---
    if not vendor:
        vendor = env["res.partner"].create({
            "name": VENDOR_NAME,
            "is_company": True,
            "supplier_rank": 1,
            "email": "ap@benchbillvendor.example.com",
        })
    else:
        vendor.write({
            "is_company": True,
            "supplier_rank": max(vendor.supplier_rank, 1),
            "email": "ap@benchbillvendor.example.com",
        })

    # --- 3. Ensure product exists as a consumable, tax-cleared. ---
    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        tmpl = env["product.template"].create({
            "name": PRODUCT_NAME,
            "type": "consu",
            "list_price": 75.0,
            "standard_price": 75.0,
            "purchase_ok": True,
            "sale_ok": True,
            # Clear default vendor taxes so the bill total is exactly 150.
            "supplier_taxes_id": [(5, 0, 0)],
            "taxes_id": [(5, 0, 0)],
        })
        product = tmpl.product_variant_id
    else:
        product.product_tmpl_id.write({
            "type": "consu",
            "list_price": 75.0,
            "standard_price": 75.0,
            "purchase_ok": True,
            "sale_ok": True,
            "supplier_taxes_id": [(5, 0, 0)],
            "taxes_id": [(5, 0, 0)],
        })

    # NOTE: We DO NOT create any draft bill. The agent must use the "New"
    # button from the vendor-bills list and fill the form from scratch.
