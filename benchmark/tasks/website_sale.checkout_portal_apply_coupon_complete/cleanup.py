"""Cleanup for website_sale.checkout_portal_apply_coupon_complete."""

PRODUCT_NAME = "Bench Coupon Item"
PROGRAM_NAME = "BENCH10"
COUPON_CODE = "BENCH10CODE"


def cleanup(env):
    admin = env.ref("base.user_admin")

    # Gather all sale orders that touch our product OR belong to admin's
    # website cart, then cancel + unlink them together with linked
    # payment transactions and invoices.
    products = env["product.template"].with_context(active_test=False).search([
        ("name", "=", PRODUCT_NAME),
    ])
    order_ids = set()
    if products:
        variant_ids = products.mapped("product_variant_ids").ids
        if variant_ids:
            ord_by_product = env["sale.order"].with_context(active_test=False).search([
                ("order_line.product_id", "in", variant_ids),
            ])
            order_ids.update(ord_by_product.ids)

    ord_by_admin = env["sale.order"].with_context(active_test=False).search([
        ("partner_id", "=", admin.partner_id.id),
        ("website_id", "!=", False),
    ])
    order_ids.update(ord_by_admin.ids)

    if order_ids:
        orders = env["sale.order"].with_context(active_test=False).browse(list(order_ids)).exists()
        for order in orders:
            txs = env["payment.transaction"].search([("sale_order_ids", "in", order.id)])
            for tx in txs:
                try:
                    tx.sudo().unlink()
                except Exception:
                    pass
            for move in order.invoice_ids:
                if move.state == "posted":
                    try:
                        move.button_draft()
                    except Exception:
                        pass
                try:
                    move.button_cancel()
                except Exception:
                    pass
                try:
                    move.sudo().unlink()
                except Exception:
                    pass
            if order.state in ("sale", "done"):
                try:
                    order.with_context(disable_cancel_warning=True)._action_cancel()
                except Exception:
                    try:
                        order.action_cancel()
                    except Exception:
                        pass
            try:
                order.sudo().unlink()
            except Exception:
                pass

    # Remove coupon cards + program.
    prog = env["loyalty.program"].with_context(active_test=False).search([
        ("name", "=", PROGRAM_NAME),
    ])
    if prog:
        cards = env["loyalty.card"].with_context(active_test=False).search([
            ("program_id", "in", prog.ids),
        ])
        if cards:
            try:
                cards.sudo().unlink()
            except Exception:
                pass
        try:
            prog.write({"active": False})
            prog.sudo().unlink()
        except Exception:
            pass

    # Any stray coupon card sharing our code.
    stray = env["loyalty.card"].with_context(active_test=False).search([
        ("code", "=", COUPON_CODE),
    ])
    if stray:
        try:
            stray.sudo().unlink()
        except Exception:
            pass

    # Finally the product.
    if products:
        try:
            products.sudo().unlink()
        except Exception:
            pass
