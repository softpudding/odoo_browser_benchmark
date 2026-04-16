"""Seed quotations for the sales credit-limit policy task.

Category 2: Policy trap.
The target quotation looks confirmable, but the customer already has an open
balance. The agent must reduce only one line quantity so the order fits within
the remaining credit before confirming.
"""


ORDER_REFS = ["CREDIT-OPS-07", "CREDIT-OPS-08"]
INVOICE_REF = "CREDIT-LIMIT-OPEN-07"


def _cleanup_invoice(env, ref):
    moves = env["account.move"].search([("ref", "=", ref)])
    for mv in moves:
        for line in mv.line_ids.filtered(
            lambda l: l.matched_debit_ids or l.matched_credit_ids
        ):
            line.remove_move_reconcile()
        if mv.state == "posted":
            mv.button_draft()
        mv.button_cancel()
        mv.unlink()


def setup(env):
    env.company.account_use_credit_limit = True

    target_partner = env["res.partner"].search(
        [("name", "=", "Atlas Field Systems")], limit=1
    )
    if not target_partner:
        target_partner = env["res.partner"].create(
            {
                "name": "Atlas Field Systems",
                "email": "billing@atlas-field.example.com",
                "credit_limit": 4000.0,
            }
        )
    else:
        target_partner.write(
            {
                "email": "billing@atlas-field.example.com",
                "credit_limit": 4000.0,
            }
        )

    distractor_partner = env["res.partner"].search(
        [("name", "=", "Atlas Fleet Services")], limit=1
    )
    if not distractor_partner:
        distractor_partner = env["res.partner"].create(
            {
                "name": "Atlas Fleet Services",
                "email": "billing@atlas-fleet.example.com",
                "credit_limit": 4000.0,
            }
        )
    else:
        distractor_partner.write(
            {
                "email": "billing@atlas-fleet.example.com",
                "credit_limit": 4000.0,
            }
        )

    for ref in ORDER_REFS:
        orders = env["sale.order"].search([("client_order_ref", "=", ref)])
        for order in orders:
            if order.state == "sale":
                order.action_cancel()
            if order.state in ("draft", "cancel"):
                order.unlink()

    _cleanup_invoice(env, INVOICE_REF)

    router = env["product.product"].search([("name", "=", "Field Router Kit")], limit=1)
    if not router:
        tmpl = env["product.template"].create(
            {
                "name": "Field Router Kit",
                "type": "consu",
                "list_price": 400.0,
            }
        )
        router = tmpl.product_variant_id

    commissioning = env["product.product"].search(
        [("name", "=", "On-site Commissioning")], limit=1
    )
    if not commissioning:
        tmpl = env["product.template"].create(
            {
                "name": "On-site Commissioning",
                "type": "service",
                "list_price": 1100.0,
                "invoice_policy": "order",
            }
        )
        commissioning = tmpl.product_variant_id

    invoice = env["account.move"].create(
        {
            "move_type": "out_invoice",
            "partner_id": target_partner.id,
            "ref": INVOICE_REF,
            "invoice_date": "2026-04-10",
            "invoice_line_ids": [
                (
                    0,
                    0,
                    {
                        "product_id": commissioning.id,
                        "quantity": 1,
                        "price_unit": 1700.0,
                        "name": "Outstanding field engineering work",
                        "tax_ids": [(5, 0, 0)],
                    },
                )
            ],
        }
    )
    invoice.action_post()

    admin = env.ref("base.user_admin")

    env["sale.order"].create(
        {
            "partner_id": target_partner.id,
            "user_id": admin.id,
            "client_order_ref": "CREDIT-OPS-07",
            "order_line": [
                (
                    0,
                    0,
                    {
                        "product_id": router.id,
                        "product_uom_qty": 4,
                        "price_unit": 400.0,
                        "tax_ids": [(5, 0, 0)],
                    },
                ),
                (
                    0,
                    0,
                    {
                        "product_id": commissioning.id,
                        "product_uom_qty": 1,
                        "price_unit": 1100.0,
                        "tax_ids": [(5, 0, 0)],
                    },
                ),
            ],
        }
    )

    env["sale.order"].create(
        {
            "partner_id": distractor_partner.id,
            "user_id": admin.id,
            "client_order_ref": "CREDIT-OPS-08",
            "order_line": [
                (
                    0,
                    0,
                    {
                        "product_id": router.id,
                        "product_uom_qty": 2,
                        "price_unit": 400.0,
                        "tax_ids": [(5, 0, 0)],
                    },
                ),
                (
                    0,
                    0,
                    {
                        "product_id": commissioning.id,
                        "product_uom_qty": 1,
                        "price_unit": 1100.0,
                        "tax_ids": [(5, 0, 0)],
                    },
                ),
            ],
        }
    )
