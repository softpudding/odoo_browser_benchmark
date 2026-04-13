"""Seed 4 quotations with different amounts for Azure Interior."""


def setup(env):
    partner = env['res.partner'].search([('name', '=', 'Azure Interior')], limit=1)
    if not partner:
        partner = env['res.partner'].create({'name': 'Azure Interior', 'email': 'azure@example.com'})

    products = {}
    for name, price in [('Large Desk', 320), ('Office Chair', 150), ('Standing Desk', 450), ('Whiteboard', 80)]:
        p = env['product.product'].search([('name', '=', name)], limit=1)
        if not p:
            tmpl = env['product.template'].create({'name': name, 'type': 'consu', 'list_price': price})
            p = tmpl.product_variant_id
        products[name] = p

    # Delete existing draft SOs for this partner to ensure clean state
    env['sale.order'].search([
        ('partner_id', '=', partner.id),
        ('state', '=', 'draft'),
    ]).unlink()

    # Create 4 quotations with known amounts
    # SO-A: $320 (1x Large Desk)
    so_a = env['sale.order'].create({'partner_id': partner.id})
    env['sale.order.line'].create({'order_id': so_a.id, 'product_id': products['Large Desk'].id, 'product_uom_qty': 1, 'price_unit': 320})

    # SO-B: $750 (5x Office Chair)
    so_b = env['sale.order'].create({'partner_id': partner.id})
    env['sale.order.line'].create({'order_id': so_b.id, 'product_id': products['Office Chair'].id, 'product_uom_qty': 5, 'price_unit': 150})

    # SO-C: $1350 (3x Standing Desk) -- THIS IS THE HIGHEST
    so_c = env['sale.order'].create({'partner_id': partner.id})
    env['sale.order.line'].create({'order_id': so_c.id, 'product_id': products['Standing Desk'].id, 'product_uom_qty': 3, 'price_unit': 450})

    # SO-D: $545 (3x Monitor Arm + 4x Whiteboard)
    so_d = env['sale.order'].create({'partner_id': partner.id})
    env['sale.order.line'].create({'order_id': so_d.id, 'product_id': products['Whiteboard'].id, 'product_uom_qty': 4, 'price_unit': 80})
    env['sale.order.line'].create({'order_id': so_d.id, 'product_id': products['Large Desk'].id, 'product_uom_qty': 1, 'price_unit': 225})
