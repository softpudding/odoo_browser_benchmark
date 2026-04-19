"""Seed for stock.run_manual_replenishment_for_product (hard).

Category 5: Deep UI interaction — Replenishment dashboard + per-row Order
button.

Seeds:
  * Vendor partner 'Bench Replenish Vendor' (supplier_rank=1).
  * Storable product 'Bench Replenish Item' (type='consu' +
    is_storable=True, tracking='none') with ONE product.supplierinfo row
    linking it to the vendor at price_unit=50.0 (seller_ids 0-0 tuple).
    On-hand = 0 at WH/Stock (no stock.quant seeded).
  * stock.warehouse.orderpoint for Bench Replenish Item at WH/Stock with
    trigger='manual' (so the Replenishment dashboard includes the row
    regardless of the default trigger filter — the Replenishment view's
    default `searchpanel_default_trigger='manual'` narrows to manual
    rules; with trigger='manual' the row is always visible), product_min_qty=5,
    product_max_qty=20. Because qty_on_hand = qty_forecast = 0 <
    min_qty=5, _compute_qty_to_order fires and qty_to_order computes
    to max(5, 20) - 0 = 20 — exactly the amount the prompt asks for.
  * Admin granted `stock.group_stock_multi_locations` so the Location
    column (and some default filters) render consistently. Replenishment
    requires `stock.group_stock_manager` (already on admin for the base
    snapshot).

Difficulty design:
  - The Replenishment dashboard is a NEW Odoo 19 entry point
    (`Inventory > Operations > Replenishment`, `/odoo/replenishment`,
    menu `stock.menu_reordering_rules_replenish`). It is *distinct* from
    the older `Inventory > Operations > Reordering Rules` menu which
    does NOT render the per-row Order/Automate buttons (those are only
    in `view_warehouse_orderpoint_tree_editable`'s `o_replenish_buttons`
    column, visible when `qty_to_order > 0.0`).
  - The agent must NOT use the dropdown `Order` menu at the top of the
    list — those items are gated by `hasSelectedRecords` and require
    ticking the row's checkbox first. The per-row fa-truck button is
    the cleaner UI path (no checkbox needed).
  - The agent must also avoid clicking **Automate** (the adjacent
    fa-refresh icon, `action_replenish_auto`) which flips `trigger` to
    `auto` and mutates the seeded orderpoint.

check.py asserts a new purchase.order exists for the vendor with one
line of qty=20 and the orderpoint stays at min=5/max=20/trigger='manual'.
"""

VENDOR_NAME = "Bench Replenish Vendor"
VENDOR_EMAIL = "orders@benchreplenish.example.com"
PRODUCT_NAME = "Bench Replenish Item"
PRICE = 50.0
MIN_QTY = 5.0
MAX_QTY = 20.0


def _cleanup(env):
    # --- Purchase orders for the vendor (from previous runs) -------------
    vendor = env["res.partner"].with_context(active_test=False).search(
        [("name", "=", VENDOR_NAME)], limit=1
    )
    if vendor:
        pos = env["purchase.order"].with_context(active_test=False).search([
            ("partner_id", "=", vendor.id),
        ])
        for po in pos:
            for p in po.picking_ids:
                if p.state not in ("done", "cancel"):
                    try:
                        p.action_cancel()
                    except Exception:
                        pass
                try:
                    p.move_ids.write({"state": "cancel"})
                    p.write({"state": "cancel"})
                    p.unlink()
                except Exception:
                    pass
            try:
                if po.state in ("purchase", "done"):
                    po.button_cancel()
                po.unlink()
            except Exception:
                pass

    # --- Orderpoints for our product (children first) -------------------
    products = env["product.product"].with_context(active_test=False).search(
        [("name", "=", PRODUCT_NAME)]
    )
    if products:
        try:
            env["stock.warehouse.orderpoint"].with_context(
                active_test=False
            ).search([("product_id", "in", products.ids)]).unlink()
        except Exception:
            pass
        try:
            env["stock.move.line"].search(
                [("product_id", "in", products.ids)]
            ).sudo().unlink()
        except Exception:
            pass
        try:
            env["stock.move"].search(
                [("product_id", "in", products.ids)]
            ).sudo().unlink()
        except Exception:
            pass
        try:
            env["stock.quant"].with_context(inventory_mode=True).search(
                [("product_id", "in", products.ids)]
            ).sudo().unlink()
        except Exception:
            pass
        try:
            env["product.supplierinfo"].search(
                [("product_tmpl_id", "in", products.mapped("product_tmpl_id").ids)]
            ).unlink()
        except Exception:
            pass
        try:
            products.mapped("product_tmpl_id").sudo().unlink()
        except Exception:
            pass

    # --- Finally, drop the vendor partner if no residual refs -----------
    if vendor:
        try:
            other_po = env["purchase.order"].search([
                ("partner_id", "=", vendor.id),
            ])
            other_bill = env["account.move"].search([
                ("partner_id", "=", vendor.id),
            ])
            if not other_po and not other_bill:
                vendor.unlink()
        except Exception:
            pass


def setup(env):
    _cleanup(env)

    # Admin: grant multi-locations group so Location column visibility is
    # deterministic in the Replenishment list.
    admin = env.ref("base.user_admin")
    admin.group_ids |= env.ref("stock.group_stock_multi_locations")

    # Vendor
    vendor = env["res.partner"].create({
        "name": VENDOR_NAME,
        "email": VENDOR_EMAIL,
        "company_type": "company",
        "supplier_rank": 1,
    })

    # Storable product + vendor pricing link (seller_ids).
    tmpl = env["product.template"].create({
        "name": PRODUCT_NAME,
        "type": "consu",
        "is_storable": True,
        "tracking": "none",
        "list_price": 75.0,
        "standard_price": PRICE,
        "sale_ok": False,
        "purchase_ok": True,
        "seller_ids": [(0, 0, {
            "partner_id": vendor.id,
            "price": PRICE,
            "min_qty": 0.0,
            "delay": 1,
        })],
    })
    product = tmpl.product_variant_id

    # On-hand = 0 at WH/Stock (no quant seeded). virtual_available is
    # also 0 since there are no pending moves, so qty_forecast = 0.

    # Locate WH/Stock internal location for the orderpoint.
    wh = env["stock.warehouse"].search([], limit=1)
    stock_loc = wh.lot_stock_id

    # Create the orderpoint (trigger=manual, min=5, max=20).
    orderpoint = env["stock.warehouse.orderpoint"].create({
        "product_id": product.id,
        "location_id": stock_loc.id,
        "warehouse_id": wh.id,
        "trigger": "manual",
        "product_min_qty": MIN_QTY,
        "product_max_qty": MAX_QTY,
    })

    # Force recompute of qty_to_order so the Replenishment dashboard sees
    # a positive "To Order" figure (which is what makes the per-row
    # fa-truck Order button visible via
    # `invisible="qty_to_order &lt;= 0.0"`).
    orderpoint._compute_qty()
    orderpoint._compute_qty_to_order_computed()
    orderpoint._compute_qty_to_order()

    env.cr.commit()
