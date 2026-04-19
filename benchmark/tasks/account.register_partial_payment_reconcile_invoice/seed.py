"""Seed two posted, unpaid customer invoices for the partial-payment task.

Category 2: Policy trap (wizard).
The agent must open the Register Payment wizard on a specific posted,
not-paid customer invoice (BENCH-PARTIAL-001, total 500.00) and override
the wizard's auto-filled amount (500.00) with a partial 200.00, then
click the primary "Create Payment" button. A second distractor invoice
(BENCH-PARTIAL-DISTRACT, total 300.00) exists for the same partner and
must remain untouched.

The trap is the wizard's default behavior: it pre-fills Amount with the
invoice's amount_residual (500.00 full). Agents that accept the default
will register a FULL payment, leaving payment_state='paid' instead of
the required 'partial'.
"""


TARGET_REF = "BENCH-PARTIAL-001"
DISTRACTOR_REF = "BENCH-PARTIAL-DISTRACT"
PARTNER_NAME = "Bench Partial Co"
SECONDARY_JOURNAL_NAME = "Bench Secondary Bank"
SECONDARY_JOURNAL_CODE = "BSB1"


def setup(env):
    # Partner
    partner = env["res.partner"].search([("name", "=", PARTNER_NAME)], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": PARTNER_NAME,
            "email": "ar@benchpartial.example.com",
        })

    company = env.company

    # Seed a SECOND bank journal with a LOWER sequence so it becomes the
    # default in the Register Payment wizard's journal_id field. The agent
    # must override the default and pick the original "Bank" journal.
    default_bank = env["account.journal"].search(
        [("company_id", "=", company.id), ("type", "=", "bank")],
        order="sequence asc, id asc",
        limit=1,
    )
    secondary = env["account.journal"].search([
        ("company_id", "=", company.id),
        ("name", "=", SECONDARY_JOURNAL_NAME),
    ], limit=1)
    lowest_seq = default_bank.sequence if default_bank else 10
    if not secondary:
        secondary = env["account.journal"].create({
            "name": SECONDARY_JOURNAL_NAME,
            "code": SECONDARY_JOURNAL_CODE,
            "type": "bank",
            "company_id": company.id,
            "sequence": max(lowest_seq - 5, 1),
        })
    else:
        secondary.write({"sequence": max(lowest_seq - 5, 1)})
    # Ensure the original Bank journal keeps its own sequence so the
    # secondary lands first in the default-pick order.
    if default_bank and default_bank.id != secondary.id:
        default_bank.write({"sequence": lowest_seq})

    # Products — two line items on the target invoice sum to 500.00.
    products = {}
    for name, price in [
        ("Bench Partial Service A", 300.0),
        ("Bench Partial Service B", 200.0),
        ("Bench Partial Distractor", 300.0),
    ]:
        prod = env["product.product"].search([("name", "=", name)], limit=1)
        if not prod:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "service",
                "list_price": price,
            })
            prod = tmpl.product_variant_id
        else:
            prod.product_tmpl_id.write({"list_price": price})
        products[name] = prod

    # Cleanup prior runs — unreconcile/cancel any related payments, reversals,
    # and the source invoices themselves.
    def _purge_move(mv):
        for line in mv.line_ids.filtered(
            lambda l: l.matched_debit_ids or l.matched_credit_ids
        ):
            line.remove_move_reconcile()
        reversals = env["account.move"].search([("reversed_entry_id", "=", mv.id)])
        for rev in reversals:
            if rev.state == "posted":
                rev.button_draft()
            rev.button_cancel()
            rev.unlink()
        if mv.state == "posted":
            mv.button_draft()
        mv.button_cancel()
        mv.unlink()

    for target_ref in (TARGET_REF, DISTRACTOR_REF):
        old = env["account.move"].search([("ref", "=", target_ref)])
        for mv in old:
            _purge_move(mv)

    # Sweep account.payment records for this partner (from prior runs)
    old_payments = env["account.payment"].search([
        ("partner_id", "=", partner.id),
    ])
    for pay in old_payments:
        move = pay.move_id
        if move:
            for line in move.line_ids.filtered(
                lambda l: l.matched_debit_ids or l.matched_credit_ids
            ):
                line.remove_move_reconcile()
        if pay.state == "posted":
            try:
                pay.action_draft()
            except Exception:
                pass
        if hasattr(pay, "action_cancel"):
            try:
                pay.action_cancel()
            except Exception:
                pass
        try:
            pay.unlink()
        except Exception:
            if pay.move_id and pay.move_id.state != "cancel":
                try:
                    pay.move_id.button_cancel()
                except Exception:
                    pass

    # Sweep any orphan customer invoices/refunds for this partner
    orphans = env["account.move"].search([
        ("partner_id", "=", partner.id),
        ("move_type", "in", ["out_invoice", "out_refund"]),
    ])
    for m in orphans:
        _purge_move(m)

    # Create and post the TARGET invoice (500.00 total, 2 lines)
    target_invoice = env["account.move"].create({
        "move_type": "out_invoice",
        "partner_id": partner.id,
        "ref": TARGET_REF,
        "invoice_date": "2026-04-10",
        "invoice_line_ids": [
            (0, 0, {
                "product_id": products["Bench Partial Service A"].id,
                "quantity": 1,
                "price_unit": 300.0,
                "name": "Bench Partial Service A",
                "tax_ids": [(5, 0, 0)],
            }),
            (0, 0, {
                "product_id": products["Bench Partial Service B"].id,
                "quantity": 1,
                "price_unit": 200.0,
                "name": "Bench Partial Service B",
                "tax_ids": [(5, 0, 0)],
            }),
        ],
    })
    target_invoice.action_post()

    # Create and post the DISTRACTOR invoice (300.00 total, 1 line).
    distractor_invoice = env["account.move"].create({
        "move_type": "out_invoice",
        "partner_id": partner.id,
        "ref": DISTRACTOR_REF,
        "invoice_date": "2026-04-10",
        "invoice_line_ids": [
            (0, 0, {
                "product_id": products["Bench Partial Distractor"].id,
                "quantity": 1,
                "price_unit": 300.0,
                "name": "Bench Partial Distractor",
                "tax_ids": [(5, 0, 0)],
            }),
        ],
    })
    distractor_invoice.action_post()
