"""Seed for sale.duplicate_quotation_edit_delivery_date_confirm.

Category: deep_ui_interaction (MEDIUM).

Seeds:
- Partner `Bench Copy Co` (no pricelist / no special config).
- Two consu products (no customer/supplier taxes for clean totals):
    * Bench SO Item A  list_price = 50.0
    * Bench SO Item B  list_price = 30.0
- A draft sale.order with `name='S-BENCH-COPY-001'` for Bench Copy Co,
  two order lines (Item A qty=2, Item B qty=3), taxes cleared.

Capability tested: duplicate a quotation via the cog/Actions menu, edit
a datetime field (`commitment_date`, labeled "Delivery Date" on the
Other Info tab) on the COPY, save, then Confirm the copy — all without
touching the original.
"""

PARTNER_NAME = "Bench Copy Co"
SOURCE_SO_NAME = "S-BENCH-COPY-001"
PRODUCT_A = "Bench SO Item A"
PRODUCT_B = "Bench SO Item B"


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

    # Also sweep any SO named S-BENCH-COPY-001 regardless of partner
    old_src = env["sale.order"].with_context(active_test=False).search(
        [("name", "=", SOURCE_SO_NAME)]
    )
    for order in old_src:
        if order.state == "sale":
            try:
                order.action_cancel()
            except Exception:
                pass
        order.sudo().unlink()

    for pname in (PRODUCT_A, PRODUCT_B):
        old_product = env["product.product"].with_context(active_test=False).search(
            [("name", "=", pname)]
        )
        if old_product:
            old_product.mapped("product_tmpl_id").sudo().unlink()

    if partner:
        partner.sudo().unlink()

    # --- Create products (no taxes → clean totals, no downstream math quirks) ---
    tmpl_a = env["product.template"].create({
        "name": PRODUCT_A,
        "type": "consu",
        "list_price": 50.0,
        "sale_ok": True,
        "taxes_id": [(5, 0, 0)],
    })
    tmpl_a.product_variant_id.product_tmpl_id.supplier_taxes_id = [(5, 0, 0)]
    product_a = tmpl_a.product_variant_id

    tmpl_b = env["product.template"].create({
        "name": PRODUCT_B,
        "type": "consu",
        "list_price": 30.0,
        "sale_ok": True,
        "taxes_id": [(5, 0, 0)],
    })
    tmpl_b.product_variant_id.product_tmpl_id.supplier_taxes_id = [(5, 0, 0)]
    product_b = tmpl_b.product_variant_id

    # --- Create partner ---
    partner = env["res.partner"].create({
        "name": PARTNER_NAME,
        "email": "bench.copy@example.com",
    })

    # --- Create the source draft quotation with the fixed name ---
    # `sale.order.name` defaults to _('New') and carries copy=False, so setting
    # it explicitly here gives us a deterministic anchor to distinguish source
    # from the duplicate (the copy will receive a fresh sequence name).
    admin = env.ref("base.user_admin")
    so = env["sale.order"].create({
        "name": SOURCE_SO_NAME,
        "partner_id": partner.id,
        "user_id": admin.id,
        # Also anchor client_order_ref; it is copy=False so the duplicate
        # will have client_order_ref=False, giving the diff engine a clean
        # way to distinguish source vs duplicate via match_key.
        "client_order_ref": SOURCE_SO_NAME,
    })

    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": product_a.id,
        "product_uom_qty": 2,
        "price_unit": 50.0,
        "tax_ids": [(5, 0, 0)],
    })
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": product_b.id,
        "product_uom_qty": 3,
        "price_unit": 30.0,
        "tax_ids": [(5, 0, 0)],
    })

    # Sanity-check state
    assert so.state == "draft", f"Seed source SO in state {so.state}"
    assert len(so.order_line) == 2, (
        f"Seed expected 2 order lines, got {len(so.order_line)}"
    )
    assert so.name == SOURCE_SO_NAME, (
        f"Seed SO name is {so.name!r}, expected {SOURCE_SO_NAME!r}"
    )
