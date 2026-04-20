"""Seed for repair.create_repair_order_add_fee_quotation_confirm."""

def setup(env):
    env["repair.order"].search([("partner_id.name", "=", "Repair Harbor")]).unlink()
    env["sale.order"].search([("partner_id.name", "=", "Repair Harbor"), ("origin", "ilike", "R")]).unlink()
    env["product.template"].search([("name", "in", ["Bench Pump Core", "Bench Diagnostic Fee"])]).unlink()
    partner = env["res.partner"].search([("name", "=", "Repair Harbor")], limit=1)
    if not partner:
        partner = env["res.partner"].create({"name": "Repair Harbor", "customer_rank": 1})
    core = env["product.product"].create({"name": "Bench Pump Core", "type": "consu", "is_storable": True, "sale_ok": True, "list_price": 220.0})
    fee = env["product.product"].create({"name": "Bench Diagnostic Fee", "type": "service", "sale_ok": True, "list_price": 35.0})
    wh = env["stock.warehouse"].search([], limit=1)
    env["stock.quant"].with_context(inventory_mode=True).create({"product_id": core.id, "location_id": wh.lot_stock_id.id, "inventory_quantity": 2}).action_apply_inventory()
    _ = fee
