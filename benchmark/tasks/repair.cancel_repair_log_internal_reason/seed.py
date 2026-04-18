"""Seed for repair.cancel_repair_log_internal_reason."""


def setup(env):
    env["repair.order"].search([("name", "=", "RO/CANCEL/0001")]).unlink()
    env["product.template"].search(
        [("name", "in", ["Bench Cooler Compressor", "Bench Cooler Belt"])]
    ).unlink()

    partner = env["res.partner"].search([("name", "=", "Cancel Cordelia")], limit=1)
    if not partner:
        partner = env["res.partner"].create(
            {"name": "Cancel Cordelia", "customer_rank": 1}
        )

    product = env["product.product"].create({
        "name": "Bench Cooler Compressor",
        "type": "consu",
        "is_storable": True,
        "sale_ok": True,
        "list_price": 480.0,
    })
    part = env["product.product"].create({
        "name": "Bench Cooler Belt",
        "type": "consu",
        "is_storable": True,
        "sale_ok": True,
        "list_price": 22.0,
    })

    warehouse = env["stock.warehouse"].search([], limit=1)
    for prod, qty in [(product, 5.0), (part, 20.0)]:
        env["stock.quant"].with_context(inventory_mode=True).create({
            "product_id": prod.id,
            "location_id": warehouse.lot_stock_id.id,
            "inventory_quantity": qty,
        }).action_apply_inventory()

    repair = env["repair.order"].create({
        "name": "RO/CANCEL/0001",
        "partner_id": partner.id,
        "product_id": product.id,
        "product_qty": 1.0,
        "picking_type_id": warehouse.repair_type_id.id,
        "move_ids": [(0, 0, {
            "product_id": part.id,
            "product_uom_qty": 1.0,
            "product_uom": part.uom_id.id,
            "repair_line_type": "add",
            "location_id": warehouse.lot_stock_id.id,
            "location_dest_id": warehouse.repair_type_id.default_location_dest_id.id or warehouse.lot_stock_id.id,
        })],
    })
    repair.action_validate()
