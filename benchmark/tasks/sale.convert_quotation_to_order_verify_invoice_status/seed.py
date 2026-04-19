"""Seed for sale.convert_quotation_to_order_verify_invoice_status.

Category: simple_confirm (EASY).

Seeds:
- Partner `Bench Confirm Co` (no pricelist / no special config).
- One consu product (taxes cleared for clean math):
    * Bench Confirm Item  list_price = 100.0
- A draft sale.order with `name='BENCH-CONFIRM'` and
  `client_order_ref='BENCH-CONFIRM'` for Bench Confirm Co, with ONE
  product order line (Bench Confirm Item qty=1 @ 100.0).

Capability tested: single-click Confirm on a draft quotation. The
quotation must transition from state='draft' to state='sale'. Distinct
from row 426 (duplicate+confirm) — here the agent just clicks the
Confirm button once. Easy anchor: calibration target ~80% pass.
"""

PARTNER_NAME = "Bench Confirm Co"
SO_NAME = "BENCH-CONFIRM"
PRODUCT_NAME = "Bench Confirm Item"


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
            order.sudo().unlink()

    # Sweep any SO named BENCH-CONFIRM regardless of partner
    old_src = env["sale.order"].with_context(active_test=False).search(
        [("name", "=", SO_NAME)]
    )
    for order in old_src:
        if order.state == "sale":
            try:
                order.action_cancel()
            except Exception:
                pass
        order.sudo().unlink()

    old_product = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    )
    if old_product:
        old_product.mapped("product_tmpl_id").sudo().unlink()

    if partner:
        partner.sudo().unlink()

    # --- Create product (no taxes → clean totals) ---
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "list_price": 100.0,
        "sale_ok": True,
        "taxes_id": [(5, 0, 0)],
    })
    tmpl.product_variant_id.product_tmpl_id.supplier_taxes_id = [(5, 0, 0)]
    product = tmpl.product_variant_id

    # --- Create partner ---
    partner = env["res.partner"].create({
        "name": PARTNER_NAME,
        "email": "bench.confirm@example.com",
    })

    # --- Create the source draft quotation with the fixed name / ref ---
    # client_order_ref is copy=False; setting it gives a stable match key
    # for the state-diff engine and a human-readable anchor.
    admin = env.ref("base.user_admin")
    so = env["sale.order"].create({
        "name": SO_NAME,
        "partner_id": partner.id,
        "user_id": admin.id,
        "client_order_ref": SO_NAME,
    })

    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": product.id,
        "product_uom_qty": 1,
        "price_unit": 100.0,
        "tax_ids": [(5, 0, 0)],
    })

    # --- Sanity-check state ---
    assert so.state == "draft", f"Seed source SO in state {so.state}"
    assert len(so.order_line) == 1, (
        f"Seed expected 1 order line, got {len(so.order_line)}"
    )
    assert so.name == SO_NAME, (
        f"Seed SO name is {so.name!r}, expected {SO_NAME!r}"
    )
    assert abs(so.amount_untaxed - 100.0) < 0.01, (
        f"Seed: expected amount_untaxed=100.0, got {so.amount_untaxed}"
    )
