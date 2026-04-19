"""Seed for sale.apply_discount_percent_on_sale_order_line.

Category: deep_ui_interaction (MEDIUM).

Sets up:
- Enables the `sale.group_discount_per_so_line` group on admin so the
  per-line Disc.% column is visible in the Order Lines list on the SO
  form. Without this group the column is hidden by default in Odoo 19,
  and the agent would have no way to edit the field via the UI.
- Partner `Bench Disc Co` (no pricelist, no special config).
- Two consu products with taxes cleared (clean downstream math):
    * Bench Product A   list_price = 50.0
    * Bench Product B   list_price = 20.0
- A draft sale.order with `name='BENCH-DISC'` and
  `client_order_ref='BENCH-DISC'` for Bench Disc Co, two product order
  lines (A qty=2 disc=0, B qty=3 disc=0), taxes cleared.

Expected end state after the task:
- Line A has discount=10.0 (qty 2 * 50 * 0.9 = 90).
- Line B unchanged (qty 3 * 20 = 60).
- amount_total = 150.0 (no taxes).
- Quotation stays in state='draft'.

Capability tested: inline Disc.% cell edit on a specific row of the
Order Lines o2m list. The trap is that the Disc.% column is hidden by
default in Odoo 19 (the `sale.group_discount_per_so_line` group controls
column visibility), so the agent depends on the seed having enabled the
group; additionally the agent must click into the correct row's
discount cell (not the second line's discount cell) and not confuse it
with the Taxes or Amount cell nearby.
"""

PARTNER_NAME = "Bench Disc Co"
SO_NAME = "BENCH-DISC"
PRODUCT_A = "Bench Product A"
PRODUCT_B = "Bench Product B"


def setup(env):
    # --- Enable per-line discount group on admin (and root for safety) ---
    # In Odoo 19 the Disc.% column on sale.order.line is gated behind
    # sale.group_discount_per_so_line. We grant the group to admin so
    # the admin login used in the benchmark sees the column.
    discount_group = env.ref(
        "sale.group_discount_per_so_line", raise_if_not_found=False
    )
    admin = env.ref("base.user_admin")
    root = env.ref("base.user_root")
    if discount_group:
        discount_group.sudo().write({
            "user_ids": [(4, admin.id), (4, root.id)],
        })

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

    # Sweep any SO named BENCH-DISC regardless of partner
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
        "list_price": 20.0,
        "sale_ok": True,
        "taxes_id": [(5, 0, 0)],
    })
    tmpl_b.product_variant_id.product_tmpl_id.supplier_taxes_id = [(5, 0, 0)]
    product_b = tmpl_b.product_variant_id

    # --- Create partner ---
    partner = env["res.partner"].create({
        "name": PARTNER_NAME,
        "email": "bench.disc@example.com",
    })

    # --- Create the source draft quotation with the fixed name/ref ---
    # client_order_ref is copy=False; setting it gives a stable key for
    # the state-diff engine and a human-readable anchor.
    so = env["sale.order"].create({
        "name": SO_NAME,
        "partner_id": partner.id,
        "user_id": admin.id,
        "client_order_ref": SO_NAME,
    })

    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": product_a.id,
        "product_uom_qty": 2,
        "price_unit": 50.0,
        "discount": 0.0,
        "tax_ids": [(5, 0, 0)],
    })
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": product_b.id,
        "product_uom_qty": 3,
        "price_unit": 20.0,
        "discount": 0.0,
        "tax_ids": [(5, 0, 0)],
    })

    # Recompute totals to be safe.
    so.invalidate_recordset()

    # Sanity-check state
    assert so.state == "draft", f"Seed source SO in state {so.state}"
    assert len(so.order_line) == 2, (
        f"Seed expected 2 order lines, got {len(so.order_line)}"
    )
    assert so.name == SO_NAME, (
        f"Seed SO name is {so.name!r}, expected {SO_NAME!r}"
    )
    # Both lines should have discount=0 at seed time.
    assert all(l.discount == 0.0 for l in so.order_line), (
        "Seed: all lines must start with discount=0.0; got "
        f"{[(l.product_id.display_name, l.discount) for l in so.order_line]}"
    )
    # Pre-discount totals: A 2*50=100, B 3*20=60 → 160 untaxed.
    assert abs(so.amount_untaxed - 160.0) < 0.01, (
        f"Seed: expected amount_untaxed=160.0, got {so.amount_untaxed}"
    )
