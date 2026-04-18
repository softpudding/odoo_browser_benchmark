"""Seed for sale_stock.deliver_partial_split_into_two_pickings.

Category: Deep UI interaction (HARD).

Creates a draft SO with TWO storable product lines where one product is
fully in stock and the other is partially available:

    - Halberd Alpha Module: 5 ordered, 5 on-hand   -> full delivery
    - Halberd Beta Module:  8 ordered, 3 on-hand   -> partial; backorder for 5

The agent must:
  1. Confirm the SO.
  2. Open the delivery and set Done = 5 for Alpha, Done = 3 for Beta.
  3. Validate, then click "Create Backorder" in the wizard.
  4. Open the new backorder picking and edit Done from the auto-reserved 5
     down to 0, then SAVE (without validating).

This exercises:
  - Inline-cell qty editing (notoriously fragile for browser-use)
  - Backorder dialog choice (default "Create Backorder")
  - A second cell-edit on the backorder (a save-without-validate)
"""


def setup(env):
    # --- Partner ---
    partner = env["res.partner"].search(
        [("name", "=", "Halberd Industries")], limit=1
    )
    if not partner:
        partner = env["res.partner"].create({
            "name": "Halberd Industries",
            "email": "ops@halberd-industries.example",
        })

    # --- Cleanup prior runs (this SO + lingering backorders) ---
    old_orders = env["sale.order"].search([
        ("client_order_ref", "=", "S-BENCH-SPLIT-001"),
    ])
    for so in old_orders:
        # Cancel + unlink any pickings (incl. backorders) tied to this SO
        for picking in so.picking_ids:
            # Recursively cancel children
            child_bos = env["stock.picking"].search([
                ("backorder_id", "=", picking.id),
            ])
            for bo in child_bos:
                if bo.state not in ("cancel", "done"):
                    try:
                        bo.action_cancel()
                    except Exception:
                        pass
                try:
                    bo.unlink()
                except Exception:
                    pass
            if picking.state not in ("cancel", "done"):
                try:
                    picking.action_cancel()
                except Exception:
                    pass
            try:
                picking.unlink()
            except Exception:
                pass
        if so.state in ("sale", "done"):
            try:
                so._action_cancel()
            except Exception:
                pass
        try:
            so.unlink()
        except Exception:
            pass

    # --- Products ---
    # NOTE: Beta has 8 on-hand (full demand) so the original picking will
    # auto-reserve all 8 — the agent MUST manually edit Beta Done from 8 -> 3
    # to force a partial split. After the partial split, 5 units of Beta will
    # remain in stock and auto-reserve onto the backorder picking, where the
    # agent must again edit Beta Done from 5 -> 0 and SAVE (no validate).
    products = {}
    for name, price, on_hand in [
        ("Halberd Alpha Module", 90.00, 5),
        ("Halberd Beta Module", 65.00, 8),
    ]:
        p = env["product.product"].search([("name", "=", name)], limit=1)
        if not p:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
                "standard_price": price,
            })
            p = tmpl.product_variant_id
        else:
            if p.product_tmpl_id.type != "consu":
                p.product_tmpl_id.write({"type": "consu"})
        if hasattr(p, "is_storable"):
            p.is_storable = True
        # Clear taxes on product template (clean math, no tax popup)
        p.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})
        products[(name)] = (p, on_hand)

    # --- Set on-hand quantities (clearing first to be deterministic) ---
    warehouse = env["stock.warehouse"].search([], limit=1)
    stock_loc = warehouse.lot_stock_id

    for name, (product, qty) in products.items():
        existing = env["stock.quant"].search([
            ("product_id", "=", product.id),
            ("location_id", "=", stock_loc.id),
        ])
        for q in existing:
            q.with_context(inventory_mode=True).write({
                "inventory_quantity": 0,
            })
            try:
                q.with_context(inventory_mode=True).action_apply_inventory()
            except Exception:
                pass

        env["stock.quant"].with_context(inventory_mode=True).create({
            "product_id": product.id,
            "location_id": stock_loc.id,
            "inventory_quantity": qty,
        }).action_apply_inventory()

    # --- Draft SO (multi-line) ---
    so = env["sale.order"].create({
        "partner_id": partner.id,
        "client_order_ref": "S-BENCH-SPLIT-001",
    })
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": products["Halberd Alpha Module"][0].id,
        "product_uom_qty": 5,
        "price_unit": 90.00,
        "tax_ids": [(5, 0, 0)],
    })
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": products["Halberd Beta Module"][0].id,
        "product_uom_qty": 8,
        "price_unit": 65.00,
        "tax_ids": [(5, 0, 0)],
    })
