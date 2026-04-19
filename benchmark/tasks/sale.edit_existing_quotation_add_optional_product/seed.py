"""Seed for sale.edit_existing_quotation_add_optional_product.

Category: deep_ui_interaction (MEDIUM).

Sets up:
- Partner `Bench Add Co` (no pricelist, no special config).
- Two consu products with taxes cleared (clean downstream math):
    * Bench Existing Item  list_price = 30.0
    * Bench Extra Item     list_price = 15.0
- A draft sale.order with `name='BENCH-ADD-LINE'` and
  `client_order_ref='BENCH-ADD-LINE'` for Bench Add Co, ONE product
  order line (Bench Existing Item qty=2 @ 30.0), taxes cleared.

Expected end state after the task:
- Line 1 (existing) UNCHANGED: Bench Existing Item qty=2 price_unit=30.0.
- Line 2 (NEW): Bench Extra Item qty=4 price_unit=15.0.
- Exactly 2 sale.order.line rows; state stays 'draft'.
- amount_untaxed = 2*30 + 4*15 = 60 + 60 = 120.

Capability tested: the agent must click the **Add a product** footer
link (default left-most option among Add a product / Add a section /
Add a note), pick the correct product `Bench Extra Item` in the new
row's product many2one dropdown, change the default qty from 1 to 4
on that same new row, and save without confirming. Traps: agent may
(a) edit the existing line's product/qty instead of appending, (b)
pick the wrong product name, (c) leave qty at the default 1, or (d)
click Confirm instead of Save.
"""

PARTNER_NAME = "Bench Add Co"
SO_NAME = "BENCH-ADD-LINE"
PRODUCT_EXISTING = "Bench Existing Item"
PRODUCT_EXTRA = "Bench Extra Item"


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

    # Sweep any SO named BENCH-ADD-LINE regardless of partner
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

    for pname in (PRODUCT_EXISTING, PRODUCT_EXTRA):
        old_product = env["product.product"].with_context(active_test=False).search(
            [("name", "=", pname)]
        )
        if old_product:
            old_product.mapped("product_tmpl_id").sudo().unlink()

    if partner:
        partner.sudo().unlink()

    # --- Create products (no taxes → clean totals, no downstream math quirks) ---
    tmpl_existing = env["product.template"].create({
        "name": PRODUCT_EXISTING,
        "type": "consu",
        "list_price": 30.0,
        "sale_ok": True,
        "taxes_id": [(5, 0, 0)],
    })
    tmpl_existing.product_variant_id.product_tmpl_id.supplier_taxes_id = [(5, 0, 0)]
    product_existing = tmpl_existing.product_variant_id

    tmpl_extra = env["product.template"].create({
        "name": PRODUCT_EXTRA,
        "type": "consu",
        "list_price": 15.0,
        "sale_ok": True,
        "taxes_id": [(5, 0, 0)],
    })
    tmpl_extra.product_variant_id.product_tmpl_id.supplier_taxes_id = [(5, 0, 0)]

    # --- Create partner ---
    partner = env["res.partner"].create({
        "name": PARTNER_NAME,
        "email": "bench.add@example.com",
    })

    # --- Create the source draft quotation with the fixed name/ref ---
    # client_order_ref is copy=False; setting it gives a stable key for
    # the state-diff engine and a human-readable anchor.
    admin = env.ref("base.user_admin")
    so = env["sale.order"].create({
        "name": SO_NAME,
        "partner_id": partner.id,
        "user_id": admin.id,
        "client_order_ref": SO_NAME,
    })

    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": product_existing.id,
        "product_uom_qty": 2,
        "price_unit": 30.0,
        "tax_ids": [(5, 0, 0)],
    })

    # Recompute totals.
    so.invalidate_recordset()

    # --- Sanity-check state ---
    assert so.state == "draft", f"Seed source SO in state {so.state}"
    assert len(so.order_line) == 1, (
        f"Seed expected 1 order line, got {len(so.order_line)}"
    )
    assert so.name == SO_NAME, (
        f"Seed SO name is {so.name!r}, expected {SO_NAME!r}"
    )
    # Pre-edit total: 2*30 = 60 untaxed.
    assert abs(so.amount_untaxed - 60.0) < 0.01, (
        f"Seed: expected amount_untaxed=60.0, got {so.amount_untaxed}"
    )
    # The Extra product must exist and have list_price = 15.0 so that
    # the new line inherits that unit price by default.
    extra = env["product.product"].search([("name", "=", PRODUCT_EXTRA)], limit=1)
    assert extra, "Seed: Bench Extra Item product was not created"
    assert abs(extra.lst_price - 15.0) < 0.01, (
        f"Seed: Bench Extra Item lst_price is {extra.lst_price}, expected 15.0"
    )
