"""Seed for sale.duplicate_confirmed_order_edit_customer.

Category: deep_ui_interaction (MEDIUM).

Seeds:
- Partners `Bench Orig Co` (owner of the seeded confirmed SO) and
  `Bench Clone Co` (the target customer the agent will switch the
  duplicate to).
- Two consu products without taxes for clean totals:
    * Bench SO Dup Item A  list_price = 40.0
    * Bench SO Dup Item B  list_price = 25.0
- A CONFIRMED sale.order with `client_order_ref='BENCH-DUP'` for
  Bench Orig Co, two order lines (A qty=2, B qty=3), `state='sale'`.

Capability tested: duplicate a CONFIRMED sale.order via the cog/Actions
menu (produces a new draft copy), change the Customer many2one on the
copy to a different partner, save the copy as a draft (do NOT confirm).

Distinct from row 426 (`sale.duplicate_quotation_edit_delivery_date_confirm`)
which duplicates a DRAFT quotation, edits `commitment_date`, and
Confirms. This one duplicates a CONFIRMED order and only changes the
customer many2one — the copy stays draft.
"""

PARTNER_ORIG = "Bench Orig Co"
PARTNER_CLONE = "Bench Clone Co"
CLIENT_REF = "BENCH-DUP"
PRODUCT_A = "Bench SO Dup Item A"
PRODUCT_B = "Bench SO Dup Item B"


def setup(env):
    # --- Cleanup prior runs (child-first) ---
    # Cancel/unlink any prior SOs carrying our client_order_ref first, before
    # touching partners (avoids FK constraint).
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

    for pname in (PARTNER_ORIG, PARTNER_CLONE):
        partner = env["res.partner"].with_context(active_test=False).search(
            [("name", "=", pname)], limit=1
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
            try:
                partner.sudo().unlink()
            except Exception:
                pass

    for pname in (PRODUCT_A, PRODUCT_B):
        old_product = env["product.product"].with_context(active_test=False).search(
            [("name", "=", pname)]
        )
        if old_product:
            try:
                old_product.mapped("product_tmpl_id").sudo().unlink()
            except Exception:
                pass

    # --- Create products (no taxes → clean totals) ---
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

    # --- Create both partners ---
    orig = env["res.partner"].create({
        "name": PARTNER_ORIG,
        "email": "bench.orig@example.com",
    })
    env["res.partner"].create({
        "name": PARTNER_CLONE,
        "email": "bench.clone@example.com",
    })

    # --- Create and CONFIRM the source sale order ---
    admin = env.ref("base.user_admin")
    so = env["sale.order"].create({
        "partner_id": orig.id,
        "user_id": admin.id,
        # client_order_ref is copy=False — seeding it here gives us a
        # deterministic anchor on the original while the duplicate has
        # client_order_ref=False (the diff engine uses this as the
        # distinguishing match_key value).
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
    assert so.partner_id.name == PARTNER_ORIG, (
        f"Seed SO partner is {so.partner_id.name!r}, expected {PARTNER_ORIG!r}"
    )
