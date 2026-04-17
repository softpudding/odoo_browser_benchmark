"""Seed posted invoices for the modify-and-reissue credit note task.

Category: policy_trap (hard).
The agent must use the "Reverse and Create Invoice" button (modify_moves)
instead of the default "Reverse" button (refund_moves) in the credit note
wizard. After the wizard creates a new draft, the agent must find it,
edit a line quantity, set the invoice date, and confirm.
"""


def setup(env):
    # --- Partners ---
    partners = {}
    for name, email in [
        ("Harborlight Engineering", "billing@harborlight-eng.example.com"),
        ("Harborlight Solutions", "billing@harborlight-sol.example.com"),
    ]:
        p = env["res.partner"].search([("name", "=", name)], limit=1)
        if not p:
            p = env["res.partner"].create({"name": name, "email": email})
        partners[name] = p

    # --- Products ---
    products = {}
    for pname, price in [
        ("Technical Audit", 200.0),
        ("Site Inspection", 150.0),
    ]:
        prod = env["product.product"].search([("name", "=", pname)], limit=1)
        if not prod:
            tmpl = env["product.template"].create({
                "name": pname,
                "type": "service",
                "list_price": price,
            })
            prod = tmpl.product_variant_id
        else:
            prod.list_price = price
        products[pname] = prod

    # --- Cleanup prior runs ---
    for ref in ["HLE-MOD-01", "HLS-DIST-01"]:
        old_moves = env["account.move"].search([("ref", "=", ref)])
        for mv in old_moves:
            # Clean any reversals
            reversals = env["account.move"].search([
                ("reversed_entry_id", "=", mv.id),
            ])
            for rev in reversals:
                # Also find new drafts created by modify (they reference the reversal)
                modify_drafts = env["account.move"].search([
                    ("reversed_entry_id", "=", rev.id),
                ])
                for md in modify_drafts:
                    if md.state == "posted":
                        md.button_draft()
                    md.button_cancel()
                    md.unlink()
                if rev.state == "posted":
                    rev.button_draft()
                rev.button_cancel()
                rev.unlink()
            for line in mv.line_ids.filtered(
                lambda l: l.matched_debit_ids or l.matched_credit_ids
            ):
                line.remove_move_reconcile()
            if mv.state == "posted":
                mv.button_draft()
            mv.button_cancel()
            mv.unlink()

    # Also clean up any draft invoices for Harborlight Engineering that
    # may have been left over from modify_moves (they won't have a ref)
    stale_drafts = env["account.move"].search([
        ("partner_id", "=", partners["Harborlight Engineering"].id),
        ("move_type", "=", "out_invoice"),
        ("state", "=", "draft"),
    ])
    for sd in stale_drafts:
        sd.button_cancel()
        sd.unlink()

    # --- Create target invoice: Harborlight Engineering ---
    target_inv = env["account.move"].create({
        "move_type": "out_invoice",
        "partner_id": partners["Harborlight Engineering"].id,
        "ref": "HLE-MOD-01",
        "invoice_date": "2026-05-15",
        "invoice_line_ids": [
            (0, 0, {
                "product_id": products["Technical Audit"].id,
                "quantity": 8,
                "price_unit": 200.0,
                "name": "Technical Audit",
                "tax_ids": [(5, 0, 0)],
            }),
            (0, 0, {
                "product_id": products["Site Inspection"].id,
                "quantity": 3,
                "price_unit": 150.0,
                "name": "Site Inspection",
                "tax_ids": [(5, 0, 0)],
            }),
        ],
    })
    target_inv.action_post()

    # --- Distractor invoice: Harborlight Solutions ---
    distractor_inv = env["account.move"].create({
        "move_type": "out_invoice",
        "partner_id": partners["Harborlight Solutions"].id,
        "ref": "HLS-DIST-01",
        "invoice_date": "2026-05-15",
        "invoice_line_ids": [
            (0, 0, {
                "product_id": products["Technical Audit"].id,
                "quantity": 4,
                "price_unit": 200.0,
                "name": "Technical Audit",
                "tax_ids": [(5, 0, 0)],
            }),
        ],
    })
    distractor_inv.action_post()
