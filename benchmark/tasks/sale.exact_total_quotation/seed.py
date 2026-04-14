"""Seed a quotation with wrong prices that the agent must fix.

Starting state: 3 lines with wrong prices
- Standing Desk: qty 2, price $450 (should be $400)
- Office Chair: qty 3, price $150 (should be $175)
- Whiteboard: qty 1, price $80 (should be $90)

Current total: 2*450 + 3*150 + 1*80 = $1430
Target total:  2*400 + 3*175 + 1*90 = $1330
"""


def setup(env):
    partner = env['res.partner'].search([('name', '=', 'Deco Addict')], limit=1)
    if not partner:
        partner = env['res.partner'].create({'name': 'Deco Addict', 'email': 'deco@example.com'})

    env['sale.order'].search([
        ('partner_id', '=', partner.id), ('state', '=', 'draft')
    ]).unlink()

    products = {}
    for name, price in [('Standing Desk', 450), ('Office Chair', 150), ('Whiteboard', 80)]:
        p = env['product.product'].search([('name', '=', name)], limit=1)
        if not p:
            t = env['product.template'].create({'name': name, 'type': 'consu', 'list_price': price})
            p = t.product_variant_id
        products[name] = p

    admin = env.ref('base.user_admin')
    so = env['sale.order'].create({'partner_id': partner.id, 'user_id': admin.id})

    # Lines with WRONG prices (default catalog prices)
    env['sale.order.line'].create({
        'order_id': so.id, 'product_id': products['Standing Desk'].id,
        'product_uom_qty': 2, 'price_unit': 450,  # should be 400
    })
    env['sale.order.line'].create({
        'order_id': so.id, 'product_id': products['Office Chair'].id,
        'product_uom_qty': 3, 'price_unit': 150,  # should be 175
    })
    env['sale.order.line'].create({
        'order_id': so.id, 'product_id': products['Whiteboard'].id,
        'product_uom_qty': 1, 'price_unit': 80,  # should be 90
    })
