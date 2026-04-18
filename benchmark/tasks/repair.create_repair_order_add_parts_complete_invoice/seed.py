"""Seed for repair.create_repair_order_add_parts_complete_invoice."""


def setup(env):
    env["repair.order"].search([("name", "=", "RO/BENCH/0001")]).unlink()
    env["sale.order"].search([("origin", "=", "RO/BENCH/0001")]).unlink()
    env["account.move"].search([("invoice_origin", "=", "RO/BENCH/0001")]).button_cancel()
    env["account.move"].search([("invoice_origin", "=", "RO/BENCH/0001")]).unlink()
    env["product.template"].search([("name", "in", ["Bench Pump Core", "Bench Repair Seal"])]).unlink()

    partner = env["res.partner"].search([("name", "=", "Repair Harbor")], limit=1)
    if not partner:
        partner = env["res.partner"].create({"name": "Repair Harbor", "customer_rank": 1})

    product = env["product.product"].create({
        "name": "Bench Pump Core",
        "type": "consu",
        "is_storable": True,
        "sale_ok": True,
        "list_price": 220.0,
    })
    part = env["product.product"].create({
        "name": "Bench Repair Seal",
        "type": "consu",
        "is_storable": True,
        "sale_ok": True,
        "list_price": 18.0,
    })

    warehouse = env["stock.warehouse"].search([], limit=1)
    for prod, qty in [(product, 3.0), (part, 10.0)]:
        env["stock.quant"].with_context(inventory_mode=True).create({
            "product_id": prod.id,
            "location_id": warehouse.lot_stock_id.id,
            "inventory_quantity": qty,
        }).action_apply_inventory()
