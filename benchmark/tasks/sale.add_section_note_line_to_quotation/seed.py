"""Seed for sale.add_section_note_line_to_quotation.

Category: deep_ui_interaction (MEDIUM).

Seeds:
- Partner `Bench Struct Co` (no pricelist, no special config).
- Two consu products with taxes cleared (clean downstream math):
    * Bench Struct Item A   list_price = 40.0
    * Bench Struct Item B   list_price = 25.0
- A draft sale.order with `name='SO-BENCH-STRUCT'` and
  `client_order_ref='SO-BENCH-STRUCT'` for Bench Struct Co, two product
  order lines (Item A qty=1, Item B qty=2), taxes cleared.

Capability tested: the agent must add two *non-product* order lines
(`display_type = 'line_section'` named 'Phase 1' and
 `display_type = 'line_note'` named 'Delivery by end of month') using the
non-default **Add a section** / **Add a note** buttons that sit next to
the default **Add a product** control in the Order Lines list footer.
The trap: the agent may instead use "Add a product" (the default,
left-most button) and leave `display_type = False`, or edit into the
wrong cell (e.g. the product many2one) rather than the section/note
name field.
"""

PARTNER_NAME = "Bench Struct Co"
SO_NAME = "SO-BENCH-STRUCT"
PRODUCT_A = "Bench Struct Item A"
PRODUCT_B = "Bench Struct Item B"


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

    # Sweep any SO named SO-BENCH-STRUCT regardless of partner
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
        "email": "bench.struct@example.com",
    })

    # --- Create the source draft quotation with the fixed name/ref ---
    # client_order_ref is copy=False; setting it gives a stable key for the
    # state-diff engine and a human-readable anchor.
    admin = env.ref("base.user_admin")
    so = env["sale.order"].create({
        "name": SO_NAME,
        "partner_id": partner.id,
        "user_id": admin.id,
        "client_order_ref": SO_NAME,
    })

    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": product_a.id,
        "product_uom_qty": 1,
        "price_unit": 40.0,
        "tax_ids": [(5, 0, 0)],
    })
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": product_b.id,
        "product_uom_qty": 2,
        "price_unit": 25.0,
        "tax_ids": [(5, 0, 0)],
    })

    # Sanity-check state
    assert so.state == "draft", f"Seed source SO in state {so.state}"
    assert len(so.order_line) == 2, (
        f"Seed expected 2 order lines, got {len(so.order_line)}"
    )
    assert so.name == SO_NAME, (
        f"Seed SO name is {so.name!r}, expected {SO_NAME!r}"
    )
    # Both seeded lines are product lines (display_type False).
    assert all(not l.display_type for l in so.order_line), (
        "Seed: product lines must start with display_type=False; got "
        f"{[(l.product_id.display_name, l.display_type) for l in so.order_line]}"
    )
