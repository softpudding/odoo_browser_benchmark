"""Seed for sale.cancel_confirmed_order_restore_draft.

Category: recovery_rollback (MEDIUM).

Seeds:
- Partner `Bench Cancel Co` (no special config).
- Two consu products without taxes for clean totals:
    * Bench Cancel Item A  list_price = 40.0
    * Bench Cancel Item B  list_price = 25.0
- A CONFIRMED sale.order with client_order_ref='BENCH-CANCEL-RESTORE' for
  Bench Cancel Co, two order lines (A qty=2, B qty=3), state='sale'.
  (No deliveries, no invoices; just a vanilla confirmed quotation, so the
  cancel flow will not launch the sale.order.cancel wizard — it calls
  action_cancel directly, which the UI wraps in a confirm dialog via the
  XML button's `confirm=...` attribute.)

Capability tested: clicking Cancel in the statusbar + confirming the
resulting native confirm dialog + then clicking Set to Quotation (only
visible once state='cancel') to return state to draft — two sequential
statusbar actions.
"""

PARTNER_NAME = "Bench Cancel Co"
CLIENT_REF = "BENCH-CANCEL-RESTORE"
PRODUCT_A = "Bench Cancel Item A"
PRODUCT_B = "Bench Cancel Item B"


def setup(env):
    # --- Cleanup prior runs (child-first) ---
    partner = env["res.partner"].with_context(active_test=False).search(
        [("name", "=", PARTNER_NAME)], limit=1
    )
    if partner:
        old_orders = env["sale.order"].with_context(active_test=False).search([
            ("partner_id", "=", partner.id),
        ])
        for order in old_orders:
            if order.state == "sale":
                try:
                    order.action_cancel()
                except Exception:
                    pass
            try:
                order.sudo().unlink()
            except Exception:
                pass

    # Sweep any SO bearing our client_order_ref (regardless of partner)
    stragglers = env["sale.order"].with_context(active_test=False).search(
        [("client_order_ref", "=", CLIENT_REF)]
    )
    for order in stragglers:
        if order.state == "sale":
            try:
                order.action_cancel()
            except Exception:
                pass
        try:
            order.sudo().unlink()
        except Exception:
            pass

    for pname in (PRODUCT_A, PRODUCT_B):
        old_product = env["product.product"].with_context(active_test=False).search(
            [("name", "=", pname)]
        )
        if old_product:
            old_product.mapped("product_tmpl_id").sudo().unlink()

    if partner:
        partner.sudo().unlink()

    # --- Create products (no taxes) ---
    tmpl_a = env["product.template"].create({
        "name": PRODUCT_A,
        "type": "consu",
        "list_price": 40.0,
        "sale_ok": True,
        "taxes_id": [(5, 0, 0)],
    })
    tmpl_a.product_variant_id.product_tmpl_id.supplier_taxes_id = [(5, 0, 0)]
    product_a = tmpl_a.product_variant_id

    tmpl_b = env["product.template"].create({
        "name": PRODUCT_B,
        "type": "consu",
        "list_price": 25.0,
        "sale_ok": True,
        "taxes_id": [(5, 0, 0)],
    })
    tmpl_b.product_variant_id.product_tmpl_id.supplier_taxes_id = [(5, 0, 0)]
    product_b = tmpl_b.product_variant_id

    # --- Create partner ---
    partner = env["res.partner"].create({
        "name": PARTNER_NAME,
        "email": "bench.cancel@example.com",
    })

    # --- Create and CONFIRM the sale order ---
    admin = env.ref("base.user_admin")
    so = env["sale.order"].create({
        "partner_id": partner.id,
        "user_id": admin.id,
        "client_order_ref": CLIENT_REF,
    })

    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": product_a.id,
        "product_uom_qty": 2,
        "price_unit": 40.0,
        "tax_ids": [(5, 0, 0)],
    })
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": product_b.id,
        "product_uom_qty": 3,
        "price_unit": 25.0,
        "tax_ids": [(5, 0, 0)],
    })

    # Confirm the order: draft → sale
    so.action_confirm()

    # Sanity checks
    assert so.state == "sale", f"Seed SO expected state='sale', got {so.state}"
    assert so.client_order_ref == CLIENT_REF, (
        f"Seed SO client_order_ref={so.client_order_ref!r}, expected {CLIENT_REF!r}"
    )
    assert len(so.order_line) == 2, (
        f"Seed expected 2 order lines, got {len(so.order_line)}"
    )
