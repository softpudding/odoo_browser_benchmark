"""Seed posted invoices for the invoice-send compose wizard task.

Category 5: Deep UI interaction.
The agent must find the right posted invoice, open the Send wizard, add a
non-default recipient, and overwrite both the subject and the HTML body before
submitting. Browser-use often leaves default recipients untouched or only
partially edits the compose modal.
"""


def _cleanup_invoice(env, ref):
    moves = env["account.move"].search([("ref", "=", ref)])
    for mv in moves:
        reversals = env["account.move"].search([("reversed_entry_id", "=", mv.id)])
        for rev in reversals:
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


def setup(env):
    for ref in ["SEND-APR-17", "SEND-APR-18"]:
        _cleanup_invoice(env, ref)

    offshore = env["res.partner"].search(
        [("name", "=", "Beacon Offshore Ltd.")], limit=1
    )
    if not offshore:
        offshore = env["res.partner"].create(
            {
                "name": "Beacon Offshore Ltd.",
                "is_company": True,
                "email": "finance@beacon-offshore.example.com",
            }
        )
    else:
        offshore.write(
            {
                "is_company": True,
                "email": "finance@beacon-offshore.example.com",
            }
        )

    controller = env["res.partner"].search(
        [("name", "=", "Beacon Offshore Controller")], limit=1
    )
    if not controller:
        controller = env["res.partner"].create(
            {
                "name": "Beacon Offshore Controller",
                "parent_id": offshore.id,
                "type": "contact",
                "email": "controller@beacon-offshore.example.com",
            }
        )
    else:
        controller.write(
            {
                "parent_id": offshore.id,
                "type": "contact",
                "email": "controller@beacon-offshore.example.com",
            }
        )

    onshore = env["res.partner"].search(
        [("name", "=", "Beacon Onshore Ltd.")], limit=1
    )
    if not onshore:
        onshore = env["res.partner"].create(
            {
                "name": "Beacon Onshore Ltd.",
                "is_company": True,
                "email": "finance@beacon-onshore.example.com",
            }
        )
    else:
        onshore.write(
            {
                "is_company": True,
                "email": "finance@beacon-onshore.example.com",
            }
        )

    product = env["product.product"].search(
        [("name", "=", "Offshore Maintenance Retainer")], limit=1
    )
    if not product:
        tmpl = env["product.template"].create(
            {
                "name": "Offshore Maintenance Retainer",
                "type": "service",
                "list_price": 2450.0,
                "invoice_policy": "order",
            }
        )
        product = tmpl.product_variant_id

    invoice_specs = [
        (offshore, "SEND-APR-17", "April offshore support retainer"),
        (onshore, "SEND-APR-18", "April onshore support retainer"),
    ]
    for partner, ref, line_name in invoice_specs:
        move = env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": partner.id,
                "ref": ref,
                "invoice_date": "2026-04-15",
                "invoice_line_ids": [
                    (
                        0,
                        0,
                        {
                            "product_id": product.id,
                            "quantity": 1,
                            "price_unit": 2450.0,
                            "name": line_name,
                            "tax_ids": [(5, 0, 0)],
                        },
                    )
                ],
            }
        )
        move.action_post()
