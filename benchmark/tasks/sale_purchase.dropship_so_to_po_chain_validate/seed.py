"""Seed for sale_purchase.dropship_so_to_po_chain_validate.

Category 1 (HARD, closed-loop cross-record): the agent must traverse a
3-record chain (Sales Order -> Purchase Order -> Dropship Picking) using
smart buttons, confirming the PO and validating the dropship transfer
along the way.

This seed:
  1. Ensures the ``stock_dropshipping`` module is installed (it is not in
     the base snapshot but is required to expose the Dropship route).
  2. Creates / refreshes a vendor, a customer, and a storable product
     wired with the Dropship route + a vendor pricelist line.
  3. Creates a confirmed sale.order S-BENCH-DS-001 with one line for 5
     units of the dropship product. Confirming the SO automatically
     creates the draft PO and the dropship picking.
"""


VENDOR_NAME = "Bench Dropship Supplier"
CUSTOMER_NAME = "Bench Dropship Buyer"
PRODUCT_NAME = "Bench Dropship Gadget"
SO_REF = "S-BENCH-DS-001"
PRICE_UNIT = 50.0
QTY = 5


def _ensure_dropshipping_module(env):
    module = env["ir.module.module"].search(
        [("name", "=", "stock_dropshipping")], limit=1
    )
    if module and module.state != "installed":
        module.button_immediate_install()


def _find_dropship_route(env):
    Route = env["stock.route"]
    # Try the well-known XML id first
    try:
        route = env.ref("stock_dropshipping.route_drop_shipping")
        if route:
            return route
    except Exception:
        pass
    # Fallback to a name search
    return Route.search([("name", "ilike", "dropship")], limit=1)


def _cleanup(env):
    # Cancel + remove any prior SO/PO/picking left from a previous run.
    so = env["sale.order"].search([("client_order_ref", "=", SO_REF)])
    for order in so:
        for picking in order.picking_ids:
            if picking.state not in ("cancel", "done"):
                picking.action_cancel()
        # Cancel any linked POs (dropship POs are linked via origin)
        linked_pos = env["purchase.order"].search([("origin", "=", order.name)])
        for po in linked_pos:
            for picking in po.picking_ids:
                if picking.state not in ("cancel", "done"):
                    picking.action_cancel()
            if po.state in ("purchase", "done"):
                po.button_cancel()
            if po.state == "cancel":
                po.button_draft()
            po.unlink()
        if order.state in ("sale", "done"):
            order._action_cancel()
        order.unlink()

    # Also tidy up any orphan PO that survived without an SO (origin matches).
    orphan_pos = env["purchase.order"].search([("origin", "=", SO_REF)])
    for po in orphan_pos:
        for picking in po.picking_ids:
            if picking.state not in ("cancel", "done"):
                picking.action_cancel()
        if po.state in ("purchase", "done"):
            po.button_cancel()
        if po.state == "cancel":
            po.button_draft()
        po.unlink()


def setup(env):
    _ensure_dropshipping_module(env)

    # --- Vendor ---
    vendor = env["res.partner"].search([("name", "=", VENDOR_NAME)], limit=1)
    if not vendor:
        vendor = env["res.partner"].create({
            "name": VENDOR_NAME,
            "email": "supplier@bench-dropship.example.com",
            "phone": "+1 555 0100",
            "street": "1 Drop Ship Way",
            "city": "Shipville",
            "zip": "12345",
            "supplier_rank": 1,
            "is_company": True,
        })
    else:
        vendor.write({"supplier_rank": 1})

    # --- Customer ---
    customer = env["res.partner"].search([("name", "=", CUSTOMER_NAME)], limit=1)
    if not customer:
        customer = env["res.partner"].create({
            "name": CUSTOMER_NAME,
            "email": "buyer@bench-dropship.example.com",
            "phone": "+1 555 0200",
            "street": "9 Buyer Lane",
            "city": "Buyertown",
            "zip": "67890",
            "customer_rank": 1,
            "is_company": True,
        })
    else:
        customer.write({"customer_rank": 1})

    dropship_route = _find_dropship_route(env)
    if not dropship_route:
        raise RuntimeError(
            "Dropship route not found even after installing stock_dropshipping"
        )

    # --- Product (storable, dropship route, vendor seller) ---
    product = env["product.product"].search([("name", "=", PRODUCT_NAME)], limit=1)
    if not product:
        tmpl_vals = {
            "name": PRODUCT_NAME,
            "type": "consu",
            "list_price": 75.0,
            "standard_price": PRICE_UNIT,
            "purchase_method": "purchase",
            "invoice_policy": "order",
            "route_ids": [(6, 0, [dropship_route.id])],
            "seller_ids": [(0, 0, {
                "partner_id": vendor.id,
                "price": PRICE_UNIT,
                "min_qty": 1.0,
            })],
        }
        tmpl = env["product.template"].create(tmpl_vals)
        product = tmpl.product_variant_id
    else:
        tmpl = product.product_tmpl_id
        tmpl.write({
            "type": "consu",
            "list_price": 75.0,
            "standard_price": PRICE_UNIT,
            "purchase_method": "purchase",
            "invoice_policy": "order",
            "route_ids": [(6, 0, [dropship_route.id])],
        })
        # Ensure exactly the one vendor seller line at our price.
        tmpl.seller_ids.unlink()
        env["product.supplierinfo"].create({
            "product_tmpl_id": tmpl.id,
            "partner_id": vendor.id,
            "price": PRICE_UNIT,
            "min_qty": 1.0,
        })
    # Mark as storable (is_storable on consu in v19 enables stock tracking).
    if "is_storable" in product._fields:
        product.is_storable = True
    # Clear taxes for clean math
    product.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})
    product.product_tmpl_id.write({"supplier_taxes_id": [(5, 0, 0)]})

    # --- Cleanup prior runs ---
    _cleanup(env)

    # --- Sale order (will auto-generate draft PO + dropship picking on confirm) ---
    so = env["sale.order"].create({
        "partner_id": customer.id,
        "client_order_ref": SO_REF,
    })
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": product.id,
        "product_uom_qty": QTY,
        "price_unit": 75.0,
        "tax_ids": [(5, 0, 0)],
    })
    so.action_confirm()

    # Sanity: confirming the SO should have produced a draft PO for the vendor
    # and a single dropship picking. We do NOT validate any of them — the
    # agent must do that.
