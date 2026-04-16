"""Seed a draft receipt for the confirm-and-validate-receipt task.

Category 2 (MEDIUM): Find a receipt, set done quantities for each line,
and validate. Setting done quantities inline requires interacting with
editable fields inside the stock move table.
"""

RECEIPT_REF = "BENCH-RCV-01"


def setup(env):
    # --- Cleanup prior runs ---
    old_picks = env["stock.picking"].search([("origin", "=", RECEIPT_REF)])
    for pick in old_picks:
        if pick.state == "done":
            # Can't delete done pickings easily, cancel first if possible
            pick.action_cancel()
        if pick.state != "done":
            pick.unlink()

    # Also clean by name pattern
    old_picks2 = env["stock.picking"].search([
        ("origin", "=", RECEIPT_REF),
    ])
    for pick in old_picks2:
        try:
            pick.action_cancel()
            pick.unlink()
        except Exception:
            pass

    # --- Ensure location ---
    location_supplier = env.ref("stock.stock_location_suppliers")
    location_stock = env["stock.location"].search(
        [("complete_name", "=", "WH/Stock")], limit=1
    )
    if not location_stock:
        location_stock = env["stock.location"].search(
            [("name", "=", "Stock"), ("usage", "=", "internal")], limit=1
        )

    # --- Ensure picking type ---
    picking_type = env["stock.picking.type"].search(
        [("code", "=", "incoming")], limit=1
    )

    # --- Ensure products ---
    products = {}
    for name, price in [("Steel Bracket 12\"", 10.0), ("Copper Wire 100m", 25.0)]:
        p = env["product.product"].search([("name", "=", name)], limit=1)
        if not p:
            tmpl = env["product.template"].create({
                "name": name,
                "type": "consu",
                "is_storable": True,
                "list_price": price,
            })
            p = tmpl.product_variant_id
        products[name] = p

    # --- Create the receipt ---
    picking = env["stock.picking"].create({
        "picking_type_id": picking_type.id,
        "location_id": location_supplier.id,
        "location_dest_id": location_stock.id,
        "origin": RECEIPT_REF,
    })

    for prod_name, qty in [("Steel Bracket 12\"", 20.0), ("Copper Wire 100m", 10.0)]:
        env["stock.move"].create({
            "name": prod_name,
            "product_id": products[prod_name].id,
            "product_uom_qty": qty,
            "picking_id": picking.id,
            "location_id": location_supplier.id,
            "location_dest_id": location_stock.id,
        })

    # Confirm the picking so it's in "Ready" state
    picking.action_confirm()
    picking.action_assign()
