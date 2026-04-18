"""Seed for sale_stock.confirm_so_manual_reserve_validate_delivery."""


TARGET_REF = "BENCH-SO-RESERVE"
DISTRACTOR_REF = "BENCH-SO-RESERVE-DIST"


def setup(env):
    partner = env["res.partner"].search([("name", "=", "Northwind Assembly")], limit=1)
    if not partner:
        partner = env["res.partner"].create({
            "name": "Northwind Assembly",
            "email": "ops@northwind-assembly.example.com",
        })

    distractor_partner = env["res.partner"].search([("name", "=", "Northwind Supplies")], limit=1)
    if not distractor_partner:
        distractor_partner = env["res.partner"].create({
            "name": "Northwind Supplies",
            "email": "sales@northwind-supplies.example.com",
        })

    for ref in (TARGET_REF, DISTRACTOR_REF):
        old_orders = env["sale.order"].search([("client_order_ref", "=", ref)])
        for so in old_orders:
            for picking in so.picking_ids.filtered(lambda p: p.state not in ("cancel", "done")):
                picking.action_cancel()
            if so.state in ("sale", "done"):
                so._action_cancel()
            so.unlink()

    products = {}
    for name, price in [
        ("Bench Servo Housing", 64.0),
        ("Bench Control Cable", 18.0),
    ]:
        product = env["product.product"].search([("name", "=", name)], limit=1)
        if not product:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "consu",
                "list_price": price,
                "standard_price": price,
            })
            product = tmpl.product_variant_id
        if hasattr(product, "is_storable"):
            product.is_storable = True
        product.product_tmpl_id.write({"taxes_id": [(5, 0, 0)]})
        products[name] = product

    warehouse = env["stock.warehouse"].search([], limit=1)
    warehouse.out_type_id.reservation_method = "manual"
    stock_loc = warehouse.lot_stock_id
    for name, qty in [("Bench Servo Housing", 25), ("Bench Control Cable", 40)]:
        env["stock.quant"].with_context(inventory_mode=True).create({
            "product_id": products[name].id,
            "location_id": stock_loc.id,
            "inventory_quantity": qty,
        }).action_apply_inventory()

    so = env["sale.order"].create({
        "name": "BENCH-RESERVE-SO",
        "partner_id": partner.id,
        "client_order_ref": TARGET_REF,
    })
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": products["Bench Servo Housing"].id,
        "product_uom_qty": 7,
        "price_unit": 64.0,
        "tax_ids": [(5, 0, 0)],
    })
    env["sale.order.line"].create({
        "order_id": so.id,
        "product_id": products["Bench Control Cable"].id,
        "product_uom_qty": 5,
        "price_unit": 18.0,
        "tax_ids": [(5, 0, 0)],
    })

    dist_so = env["sale.order"].create({
        "name": "BENCH-RESERVE-DIST-SO",
        "partner_id": distractor_partner.id,
        "client_order_ref": DISTRACTOR_REF,
    })
    env["sale.order.line"].create({
        "order_id": dist_so.id,
        "product_id": products["Bench Servo Housing"].id,
        "product_uom_qty": 3,
        "price_unit": 64.0,
        "tax_ids": [(5, 0, 0)],
    })
