"""Seed for stock.internal_transfer_between_locations.

Ensures:
- Product 'Benchmark Shelf Widget' exists with 5 units on hand at WH/Stock.
- Sub-location 'WH/Stock/Shelf A1' exists.
- Internal transfer picking type is active for WH.
- No prior transfer with origin BENCH-INT-SHELF-A1 exists.
"""

PRODUCT_NAME = "Benchmark Shelf Widget"
ORIGIN = "BENCH-INT-SHELF-A1"
SUBLOC_NAME = "Shelf A1"


def setup(env):
    # Cleanup prior runs.
    prior = env["stock.picking"].search([("origin", "=", ORIGIN)])
    for p in prior:
        if p.state not in ("done", "cancel"):
            try:
                p.action_cancel()
            except Exception:
                pass
    prior.filtered(lambda p: p.state != "done").unlink()

    # Ensure internal transfers are enabled on the main warehouse.
    warehouse = env["stock.warehouse"].search([("code", "=", "WH")], limit=1)
    if warehouse and not warehouse.int_type_id.active:
        warehouse.int_type_id.active = True
    # Some seeds need the multi-step features off, but for a simple
    # single-step internal transfer no further config is required.

    # Ensure WH/Stock location exists and sub-location Shelf A1 under it.
    stock_loc = env["stock.location"].search([
        ("complete_name", "=", "WH/Stock"),
    ], limit=1)
    if not stock_loc:
        stock_loc = env["stock.location"].search([
            ("name", "=", "Stock"),
            ("usage", "=", "internal"),
        ], limit=1)
    if not stock_loc:
        return  # Base snapshot must have WH/Stock; abort if missing.

    shelf = env["stock.location"].search([
        ("location_id", "=", stock_loc.id),
        ("name", "=", SUBLOC_NAME),
    ], limit=1)
    if not shelf:
        env["stock.location"].create({
            "name": SUBLOC_NAME,
            "location_id": stock_loc.id,
            "usage": "internal",
        })

    # Ensure product exists as a storable.
    product = env["product.product"].search([
        ("name", "=", PRODUCT_NAME),
    ], limit=1)
    if not product:
        tmpl = env["product.template"].create({
            "name": PRODUCT_NAME,
            "type": "consu",
            "is_storable": True,
            "tracking": "none",
        })
        product = tmpl.product_variant_id

    # Set 5 units on hand at WH/Stock using an inventory adjustment.
    quant = env["stock.quant"].with_context(inventory_mode=True).search([
        ("product_id", "=", product.id),
        ("location_id", "=", stock_loc.id),
    ], limit=1)
    if quant:
        quant.inventory_quantity = 5.0
    else:
        quant = env["stock.quant"].with_context(inventory_mode=True).create({
            "product_id": product.id,
            "location_id": stock_loc.id,
            "inventory_quantity": 5.0,
        })
    try:
        quant.action_apply_inventory()
    except Exception:
        pass
