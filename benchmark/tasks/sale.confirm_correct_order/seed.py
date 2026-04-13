"""Create two similar quotations for Gemini Furniture."""


def setup(env):
    partner = env['res.partner'].search([('name', '=', 'Gemini Furniture')], limit=1)
    if not partner:
        partner = env['res.partner'].create({'name': 'Gemini Furniture', 'email': 'gemini@example.com'})

    standing = env['product.product'].search([('name', '=', 'Standing Desk')], limit=1)
    if not standing:
        t = env['product.template'].create({'name': 'Standing Desk', 'type': 'consu', 'list_price': 450})
        standing = t.product_variant_id

    chair = env['product.product'].search([('name', '=', 'Office Chair')], limit=1)
    if not chair:
        t = env['product.template'].create({'name': 'Office Chair', 'type': 'consu', 'list_price': 150})
        chair = t.product_variant_id

    # Remove existing draft SOs for clean state
    env['sale.order'].search([
        ('partner_id', '=', partner.id),
        ('state', '=', 'draft'),
    ]).unlink()

    # Create two quotations
    so_standing = env['sale.order'].create({'partner_id': partner.id})
    env['sale.order.line'].create({
        'order_id': so_standing.id,
        'product_id': standing.id,
        'product_uom_qty': 2,
        'price_unit': 450,
    })

    so_chair = env['sale.order'].create({'partner_id': partner.id})
    env['sale.order.line'].create({
        'order_id': so_chair.id,
        'product_id': chair.id,
        'product_uom_qty': 3,
        'price_unit': 150,
    })
