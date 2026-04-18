"""Seed for inventory.run_replenishment_from_dashboard.

MEDIUM (deep_ui_interaction): Run replenishment for a low-stock product from the
Inventory > Operations > Replenishment dashboard. Seed creates:

* Vendor "Bench Supplies Ltd" (supplier_rank=1).
* Storable product "Bench Reorder Widget" with the vendor as a seller and the
  Buy route enabled. on-hand quantity = 2 in main warehouse stock location.
* A manual orderpoint (reordering rule) for the product (min=10, max=30).

The agent must navigate to the Replenishment dashboard and click Order on that
row, producing a draft purchase.order for 28 units.
"""

VENDOR_NAME = "Bench Supplies Ltd"
PRODUCT_NAME = "Bench Reorder Widget"
ORDERPOINT_MIN = 10.0
ORDERPOINT_MAX = 30.0
ON_HAND_QTY = 2.0
LIST_PRICE = 25.0
STANDARD_PRICE = 10.0


def _cleanup(env):
    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if vendor:
        # Cancel/unlink any prior POs from this vendor (any state).
        prior_pos = env["purchase.order"].search([("partner_id", "=", vendor.id)])
        for po in prior_pos:
            for pick in po.picking_ids.filtered(
                lambda p: p.state not in ("done", "cancel")
            ):
                pick.action_cancel()
            if po.state in ("purchase", "done"):
                po.button_cancel()
            if po.state == "cancel":
                po.button_draft()
            po.unlink()

    products = env["product.product"].search([("name", "=", PRODUCT_NAME)])
    if products:
        env["stock.warehouse.orderpoint"].search([
            ("product_id", "in", products.ids)
        ]).unlink()
        # Clear any quants for this product.
        env["stock.quant"].search([("product_id", "in", products.ids)]).unlink()
        # Clear stock moves so the product can be unlinked safely.
        moves = env["stock.move"].search([("product_id", "in", products.ids)])
        if moves:
            moves.filtered(lambda m: m.state not in ("done", "cancel"))._action_cancel()
        # Best-effort: leave product alone if other moves keep it referenced.
        try:
            products.product_tmpl_id.unlink()
        except Exception:
            # If unlink fails (e.g., done moves), just rewrite essential fields.
            pass


def _ensure_vendor(env):
    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if vendor:
        vendor.write({"supplier_rank": 1})
        return vendor
    return env["res.partner"].create({
        "name": VENDOR_NAME,
        "email": "buying@bench-supplies.example.com",
        "supplier_rank": 1,
        "company_type": "company",
    })


def _ensure_product(env, vendor):
    buy_route = env.ref("purchase_stock.route_warehouse0_buy", raise_if_not_found=False)
    product = env["product.product"].search([("name", "=", PRODUCT_NAME)], limit=1)
    vals = {
        "name": PRODUCT_NAME,
        "is_storable": True,
        "list_price": LIST_PRICE,
        "standard_price": STANDARD_PRICE,
        "purchase_ok": True,
        "sale_ok": True,
    }
    if buy_route:
        vals["route_ids"] = [(6, 0, [buy_route.id])]

    if not product:
        tmpl = env["product.template"].create(vals)
        product = tmpl.product_variant_id
    else:
        product.product_tmpl_id.write(vals)

    # Ensure vendor seller line.
    seller = env["product.supplierinfo"].search([
        ("partner_id", "=", vendor.id),
        ("product_tmpl_id", "=", product.product_tmpl_id.id),
    ], limit=1)
    if not seller:
        env["product.supplierinfo"].create({
            "partner_id": vendor.id,
            "product_tmpl_id": product.product_tmpl_id.id,
            "price": STANDARD_PRICE,
            "min_qty": 1,
        })
    return product


def _set_on_hand(env, product, location, qty):
    # Wipe existing quants for the product at this location, then set fresh.
    env["stock.quant"].search([
        ("product_id", "=", product.id),
        ("location_id", "=", location.id),
    ]).unlink()
    env["stock.quant"].with_context(inventory_mode=True).create({
        "product_id": product.id,
        "location_id": location.id,
        "inventory_quantity": qty,
    }).action_apply_inventory()


def _ensure_orderpoint(env, product, location, warehouse):
    op = env["stock.warehouse.orderpoint"].search([
        ("product_id", "=", product.id),
    ], limit=1)
    vals = {
        "product_id": product.id,
        "location_id": location.id,
        "warehouse_id": warehouse.id,
        "product_min_qty": ORDERPOINT_MIN,
        "product_max_qty": ORDERPOINT_MAX,
        "trigger": "manual",
    }
    if op:
        op.write(vals)
        return op
    return env["stock.warehouse.orderpoint"].create(vals)


def setup(env):
    _cleanup(env)

    warehouse = env["stock.warehouse"].search([], limit=1)
    location = warehouse.lot_stock_id

    vendor = _ensure_vendor(env)
    product = _ensure_product(env, vendor)
    _set_on_hand(env, product, location, ON_HAND_QTY)
    op = _ensure_orderpoint(env, product, location, warehouse)
    # Force qty_to_order to recompute so the dashboard shows the row.
    op._compute_qty()
    op._compute_qty_to_order()
