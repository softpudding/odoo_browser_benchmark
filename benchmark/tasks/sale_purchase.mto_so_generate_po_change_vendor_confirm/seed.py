"""Seed for sale_purchase.mto_so_generate_po_change_vendor_confirm.

Category 1 (HARD, closed-loop cross-module):
    - Confirming a sale order for a MTO+Buy product auto-generates a draft
      Request for Quotation (RFQ) for the *first* configured vendor.  The
      agent must follow the SO -> Purchase smart-button chain to the
      auto-generated RFQ, swap its ``partner_id`` from the default vendor
      (Acme Supply Co) to an alternative (Brook Trading Ltd) so the line
      ``price_unit`` recomputes from the second vendor's pricelist, and
      then confirm the PO.

Prerequisites:
    - Modules ``sale_stock``, ``purchase_stock``, ``sale_purchase``,
      ``sale_purchase_stock`` are auto-installed in the benchmark base
      (``purchase`` + ``sale_service`` + ``stock`` are root modules).
    - The MTO route (``stock.route_warehouse0_mto``) ships with
      ``active=False`` — seed must activate it.

This seed:
    1. Ensures the MTO route is active + enables "Multi-step Routes"
       on the main company (needed for per-product route selection UI).
    2. Creates / refreshes two vendor partners (Acme Supply Co,
       Brook Trading Ltd) and a customer (Bench MTO Customer).
    3. Creates a storable product ``Bench MTO Widget`` wired with
       routes = [Buy, MTO] and two ``product.supplierinfo`` rows
       (Acme 50.00 / sequence=1, Brook 40.00 / sequence=2).
    4. Creates sale order ``S-BENCH-MTO-001`` with one line of
       5 x Bench MTO Widget @ 80.00, then ``action_confirm``s it so the
       MTO procurement auto-generates the draft RFQ for Acme.
    5. Verifies that exactly one RFQ was generated, owned by Acme.
"""


VENDOR_A = "Acme Supply Co"
VENDOR_B = "Brook Trading Ltd"
CUSTOMER_NAME = "Bench MTO Customer"
PRODUCT_NAME = "Bench MTO Widget"
SO_REF = "S-BENCH-MTO-001"
SO_NAME = "S-BENCH-MTO-001"
SALE_PRICE = 80.0
PRICE_A = 50.0
PRICE_B = 40.0
QTY = 5


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


def _find_mto_route(env):
    try:
        route = env.ref("stock.route_warehouse0_mto")
    except Exception:
        route = env["stock.route"].search(
            [("name", "ilike", "MTO")], limit=1
        )
    return route


def _cleanup(env, customer, vendors):
    # --- Sale orders (by customer AND by name) ---
    sos = env["sale.order"].with_context(active_test=False).search([
        "|", "|",
        ("name", "=", SO_NAME),
        ("client_order_ref", "=", SO_REF),
        ("partner_id", "=", customer.id),
    ])
    for so in sos:
        # Cancel linked POs first (MTO PO carries sale_line_id)
        linked_pos = env["purchase.order"].with_context(active_test=False).search([
            "|",
            ("origin", "=", so.name),
            ("order_line.sale_line_id.order_id", "=", so.id),
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

        for picking in so.picking_ids:
            if picking.state not in ("cancel", "done"):
                try:
                    picking.action_cancel()
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

    # --- Orphan POs for our vendors (from prior aborted runs) ---
    for v in vendors:
        pos = env["purchase.order"].with_context(active_test=False).search([
            ("partner_id", "=", v.id),
        ])
        for po in pos:
            # Only drop POs that look like ours (origin matches or linked to our SO name)
            if po.origin and SO_NAME not in (po.origin or ""):
                # Also check sale_line_id chain
                if not any(
                    (pl.sale_line_id and pl.sale_line_id.order_id.name == SO_NAME)
                    for pl in po.order_line
                ):
                    continue
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
    # --- 1. Activate MTO route + Buy route (product-selectable) ---
    # The MTO route ships with active=False in fresh DBs.  The Buy route
    # exists but is warehouse-selectable only — flipping it to
    # product_selectable=True matches the canonical "MTO + Buy on the
    # product" pattern used in sale_purchase_stock tests.
    mto_route = env.ref("stock.route_warehouse0_mto")
    mto_route.active = True

    buy_route = env.ref("purchase_stock.route_warehouse0_buy")
    buy_route.product_selectable = True

    # Ensure Buy is the default resupply on the main warehouse.
    main_wh = env["stock.warehouse"].search([], limit=1)
    if not main_wh:
        raise RuntimeError("No stock.warehouse found")
    if not main_wh.buy_to_resupply:
        main_wh.buy_to_resupply = True
    # Re-sync warehouse routes so the MTO pull rule is created/updated
    # after we toggle MTO active.
    route_vals = main_wh._create_or_update_route()
    if route_vals:
        main_wh.write(route_vals)
    # Force all MTO-route rules to procure_method='make_to_order' (the
    # default for new rules; this is a no-op in most DBs but protects
    # against re-runs against an existing warehouse where the rule was
    # demoted to 'make_to_stock' earlier).
    mto_route.rule_ids.write({"procure_method": "make_to_order"})

    # Multi-step route group makes route_ids editable on product forms.
    grp_multi = env.ref("stock.group_adv_location", raise_if_not_found=False)
    if grp_multi:
        admin = env.ref("base.user_admin")
        if admin not in grp_multi.user_ids:
            grp_multi.user_ids = [(4, admin.id)]

    # --- 2. Partners ---
    vendor_a = _ensure_vendor(env, VENDOR_A, "sales@acme.example.com")
    vendor_b = _ensure_vendor(env, VENDOR_B, "orders@brook.example.com")
    customer = _ensure_customer(
        env, CUSTOMER_NAME, "buyer@bench-mto.example.com"
    )

    # --- 3. Product ---
    product = env["product.product"].search(
        [("name", "=", PRODUCT_NAME)], limit=1
    )
    if not product:
        tmpl = env["product.template"].create({
            "name": PRODUCT_NAME,
            "type": "consu",
            "is_storable": True,
            "list_price": SALE_PRICE,
            "standard_price": PRICE_A,
            "purchase_method": "purchase",
            "invoice_policy": "order",
            "purchase_ok": True,
            "sale_ok": True,
            "route_ids": [(6, 0, [mto_route.id, buy_route.id])],
        })
        product = tmpl.product_variant_id
    else:
        tmpl = product.product_tmpl_id
        tmpl.write({
            "type": "consu",
            "is_storable": True,
            "list_price": SALE_PRICE,
            "standard_price": PRICE_A,
            "purchase_method": "purchase",
            "invoice_policy": "order",
            "purchase_ok": True,
            "sale_ok": True,
            "route_ids": [(6, 0, [mto_route.id, buy_route.id])],
        })

    # Clear taxes for clean math.
    tmpl.write({
        "taxes_id": [(5, 0, 0)],
        "supplier_taxes_id": [(5, 0, 0)],
    })

    # Supplierinfo: Acme first (sequence=1, price 50), Brook second (sequence=2, price 40).
    tmpl.seller_ids.unlink()
    env["product.supplierinfo"].create([
        {
            "product_tmpl_id": tmpl.id,
            "partner_id": vendor_a.id,
            "price": PRICE_A,
            "min_qty": 1.0,
            "sequence": 1,
        },
        {
            "product_tmpl_id": tmpl.id,
            "partner_id": vendor_b.id,
            "price": PRICE_B,
            "min_qty": 1.0,
            "sequence": 2,
        },
    ])

    # --- 4. Cleanup prior runs ---
    _cleanup(env, customer, vendor_a + vendor_b)

    # --- 5. Create + confirm SO (MTO procurement auto-generates PO) ---
    so = env["sale.order"].create({
        "name": SO_NAME,
        "partner_id": customer.id,
        "client_order_ref": SO_REF,
    })
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": product.id,
        "product_uom_qty": QTY,
        "price_unit": SALE_PRICE,
        "tax_ids": [(5, 0, 0)],
    })
    so.action_confirm()

    # --- 6. Sanity: exactly one draft RFQ for Acme Supply Co ---
    # For the MTO+Buy flow (non-dropship) the generated PO line does NOT
    # carry ``sale_line_id`` (that field is only populated for dropship).
    # Link the PO to the SO via ``origin`` (SO.name) instead.
    pos = env["purchase.order"].search([
        ("origin", "=", so.name),
    ])
    if len(pos) != 1:
        raise RuntimeError(
            f"Expected exactly 1 MTO-generated PO with origin='{so.name}', "
            f"got {len(pos)} (ids={pos.ids})"
        )
    if pos.partner_id != vendor_a:
        raise RuntimeError(
            f"Expected generated PO vendor to be '{VENDOR_A}', "
            f"got '{pos.partner_id.name}'"
        )
    if pos.state != "draft":
        raise RuntimeError(
            f"Expected generated PO state 'draft', got '{pos.state}'"
        )
