"""Seed for sale_purchase.mto_so_generate_po_change_vendor_confirm."""


VENDOR_A = "Atlas Components"
VENDOR_B = "Beacon Components"
CUSTOMER_NAME = "Northwind MTO"
PRODUCT_NAME = "Bench Relay Module"
SO_REF = "MTO-VENDOR-SWITCH"
QTY = 3.0
PRICE_A = 70.0
PRICE_B = 62.0


def _ensure_vendor(env, name, email):
    partner = env["res.partner"].search([("name", "=", name)], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": name,
            "email": email,
            "supplier_rank": 1,
            "is_company": True,
        })
    else:
        partner.write({"supplier_rank": max(partner.supplier_rank, 1)})
    return partner


def _cleanup(env):
    orders = env["sale.order"].with_context(active_test=False).search([
        ("client_order_ref", "=", SO_REF),
    ])
    for order in orders:
        linked_pos = env["purchase.order"].with_context(active_test=False).search([
            ("origin", "=", order.name),
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
        order.unlink()

    orphan_pos = env["purchase.order"].with_context(active_test=False).search([
        ("origin", "=", SO_REF),
    ])
    for po in orphan_pos:
        try:
            po.unlink()
        except Exception:
            pass


def setup(env):
    customer = env["res.partner"].search([("name", "=", CUSTOMER_NAME)], limit=1)
    if not customer:
        customer = env["res.partner"].create({
            "name": CUSTOMER_NAME,
            "customer_rank": 1,
            "is_company": True,
            "email": "orders@northwind-mto.test",
        })
    else:
        customer.write({"customer_rank": max(customer.customer_rank, 1)})

    vendor_a = _ensure_vendor(env, VENDOR_A, "purchasing@atlas-components.test")
    vendor_b = _ensure_vendor(env, VENDOR_B, "sales@beacon-components.test")

    route_mto = env.ref("stock.route_warehouse0_mto", raise_if_not_found=False)
    buy_route = env.ref("purchase_stock.route_warehouse0_buy", raise_if_not_found=False)
    if route_mto:
        route_mto.active = True
        route_mto.product_selectable = True
        route_mto.product_categ_selectable = True
    if not route_mto or not buy_route:
        raise RuntimeError("MTO or Buy route not found")

    product = env["product.product"].search([("name", "=", PRODUCT_NAME)], limit=1)
    tmpl_vals = {
        "name": PRODUCT_NAME,
        "type": "consu",
        "sale_ok": True,
        "purchase_ok": True,
        "list_price": 110.0,
        "standard_price": PRICE_B,
        "invoice_policy": "order",
        "taxes_id": [(5, 0, 0)],
        "supplier_taxes_id": [(5, 0, 0)],
        "route_ids": [(6, 0, [route_mto.id, buy_route.id])],
    }
    if product:
        product.product_tmpl_id.write(tmpl_vals)
        tmpl = product.product_tmpl_id
    else:
        tmpl = env["product.template"].create(tmpl_vals)
        product = tmpl.product_variant_id

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
            "sequence": 10,
        },
    ])

    _cleanup(env)

    so = env["sale.order"].create({
        "partner_id": customer.id,
        "client_order_ref": SO_REF,
    })
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": product.id,
        "product_uom_qty": QTY,
        "price_unit": 110.0,
        "tax_ids": [(5, 0, 0)],
    })
