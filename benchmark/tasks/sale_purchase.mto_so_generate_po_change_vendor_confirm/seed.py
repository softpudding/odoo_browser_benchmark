"""Seed for sale_purchase.mto_so_generate_po_change_vendor_confirm.

Category 1 (HARD, closed-loop cross-module): confirm an MTO sale order,
navigate via the Purchase smart button to the auto-generated RFQ, switch
the vendor to a different approved supplier, and confirm the PO.

This seed:
  1. Ensures the Buy and Replenish-on-Order (MTO) routes are active.
  2. Creates / refreshes a customer and two vendors.
  3. Creates a storable product wired with:
        - route_ids = [Buy, MTO]
        - seller_ids = [Alpha Precision Parts (primary),
                        Orion Component Works (alternative)]
  4. Creates a DRAFT sale.order S-BENCH-MTO-001 with one line for 8 units of
     the MTO product at 150.00 (taxes cleared). The agent must confirm this
     SO, which auto-creates a draft RFQ for Alpha Precision Parts (the
     primary seller).
"""


VENDOR_PRIMARY = "Alpha Precision Parts"
VENDOR_ALT = "Orion Component Works"
CUSTOMER_NAME = "Harbor MTO Buyer"
PRODUCT_NAME = "Harbor MTO Gadget"
SO_REF = "S-BENCH-MTO-001"
PRICE_UNIT = 150.0
QTY = 8


def _find_buy_route(env):
    Route = env["stock.route"]
    route = env.ref(
        "purchase_stock.route_warehouse0_buy", raise_if_not_found=False
    )
    if route:
        return route
    return Route.search([("name", "=", "Buy")], limit=1)


def _find_mto_route(env):
    Route = env["stock.route"]
    route = env.ref(
        "stock.route_warehouse0_mto", raise_if_not_found=False
    )
    if route:
        # MTO route is inactive by default; activate it.
        if not route.active:
            route.active = True
        return route
    # Fallback name search (may be translated as "Replenish on Order (MTO)").
    route = Route.with_context(active_test=False).search(
        [("name", "ilike", "MTO")], limit=1
    )
    if route and not route.active:
        route.active = True
    return route


def _ensure_vendor(env, name, email):
    p = env["res.partner"].search([("name", "=", name)], limit=1)
    if not p:
        p = env["res.partner"].create({
            "name": name,
            "email": email,
            "supplier_rank": 1,
            "is_company": True,
        })
    else:
        p.write({"supplier_rank": max(p.supplier_rank, 1)})
    return p


def _ensure_customer(env, name, email):
    p = env["res.partner"].search([("name", "=", name)], limit=1)
    if not p:
        p = env["res.partner"].create({
            "name": name,
            "email": email,
            "customer_rank": 1,
            "is_company": True,
        })
    else:
        p.write({"customer_rank": max(p.customer_rank, 1)})
    return p


def _cleanup(env):
    # Any SO / PO / picking from prior runs of this task.
    sos = env["sale.order"].search([("client_order_ref", "=", SO_REF)])
    so_names = sos.mapped("name")

    for order in sos:
        for picking in order.picking_ids:
            if picking.state not in ("cancel", "done"):
                try:
                    picking.action_cancel()
                except Exception:
                    pass

        linked_pos = env["purchase.order"].search([
            ("origin", "in", list(set(so_names + [SO_REF])) or [SO_REF]),
        ])
        for po in linked_pos:
            for picking in po.picking_ids:
                if picking.state not in ("cancel", "done"):
                    try:
                        picking.action_cancel()
                    except Exception:
                        pass
            if po.state in ("purchase", "done"):
                try:
                    po.button_cancel()
                except Exception:
                    pass
            if po.state == "cancel":
                try:
                    po.button_draft()
                except Exception:
                    pass
            try:
                po.unlink()
            except Exception:
                pass

        if order.state in ("sale", "done"):
            try:
                order._action_cancel()
            except Exception:
                pass
        try:
            order.unlink()
        except Exception:
            pass

    # Orphan POs whose origin literally equals the SO client ref (rare).
    orphans = env["purchase.order"].search([("origin", "=", SO_REF)])
    for po in orphans:
        for picking in po.picking_ids:
            if picking.state not in ("cancel", "done"):
                try:
                    picking.action_cancel()
                except Exception:
                    pass
        if po.state in ("purchase", "done"):
            try:
                po.button_cancel()
            except Exception:
                pass
        if po.state == "cancel":
            try:
                po.button_draft()
            except Exception:
                pass
        try:
            po.unlink()
        except Exception:
            pass


def setup(env):
    buy_route = _find_buy_route(env)
    if not buy_route:
        raise RuntimeError("Buy route not found — purchase_stock may be missing")
    mto_route = _find_mto_route(env)
    if not mto_route:
        raise RuntimeError(
            "MTO route (Replenish on Order) not found — base stock module missing?"
        )

    vendor_primary = _ensure_vendor(env, VENDOR_PRIMARY, "orders@alpha-precision.example.com")
    vendor_alt = _ensure_vendor(env, VENDOR_ALT, "orders@orion-components.example.com")
    customer = _ensure_customer(env, CUSTOMER_NAME, "buyer@harbor-mto.example.com")

    # --- Product (storable, routes = Buy + MTO, two vendors) ---
    product = env["product.product"].search([("name", "=", PRODUCT_NAME)], limit=1)
    tmpl_vals = {
        "name": PRODUCT_NAME,
        "type": "consu",
        "list_price": 220.0,
        "standard_price": PRICE_UNIT,
        "purchase_method": "purchase",
        "invoice_policy": "order",
        "route_ids": [(6, 0, [buy_route.id, mto_route.id])],
    }
    if not product:
        tmpl = env["product.template"].create(tmpl_vals)
        product = tmpl.product_variant_id
    else:
        tmpl = product.product_tmpl_id
        tmpl.write(tmpl_vals)
        # Wipe seller lines so we can recreate them deterministically with
        # the correct priority ordering.
        tmpl.seller_ids.unlink()

    tmpl = product.product_tmpl_id
    # Re-create supplier lines in the desired order: primary first, alt second.
    # sequence controls which vendor the MTO rule picks (lowest sequence wins).
    env["product.supplierinfo"].create({
        "product_tmpl_id": tmpl.id,
        "partner_id": vendor_primary.id,
        "price": PRICE_UNIT,
        "min_qty": 1.0,
        "sequence": 1,
    })
    env["product.supplierinfo"].create({
        "product_tmpl_id": tmpl.id,
        "partner_id": vendor_alt.id,
        "price": PRICE_UNIT + 10.0,  # slightly higher to make "primary" obvious
        "min_qty": 1.0,
        "sequence": 10,
    })

    # Mark as storable so stock tracking / MTO procurement engages.
    if "is_storable" in product._fields:
        product.is_storable = True
    # Clear taxes for clean math.
    tmpl.write({
        "taxes_id": [(5, 0, 0)],
        "supplier_taxes_id": [(5, 0, 0)],
    })

    # --- Cleanup prior runs (must be AFTER product exists so its
    # partner links resolve, but BEFORE we create a fresh SO) ---
    _cleanup(env)

    # --- Draft sale order with one line. The agent confirms this. ---
    so = env["sale.order"].create({
        "partner_id": customer.id,
        "client_order_ref": SO_REF,
    })
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": product.id,
        "product_uom_qty": QTY,
        "price_unit": PRICE_UNIT,
        "tax_ids": [(5, 0, 0)],
    })
    # NOTE: do NOT confirm — agent must click Confirm to trigger MTO PO
    # generation.
