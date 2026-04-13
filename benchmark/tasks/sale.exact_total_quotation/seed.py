"""Ensure products and customer exist."""


def setup(env):
    partner = env['res.partner'].search([('name', '=', 'Deco Addict')], limit=1)
    if not partner:
        partner = env['res.partner'].create({'name': 'Deco Addict', 'email': 'deco@example.com'})
    # Clean up any existing draft SOs from previous runs
    env['sale.order'].search([('partner_id', '=', partner.id), ('state', '=', 'draft')]).unlink()

    for name, price in [
        ('Large Desk', 320), ('Office Chair', 150), ('Standing Desk', 450),
        ('Keyboard Tray', 45), ('Desk Lamp', 60), ('Monitor Arm', 75),
        ('Cable Manager', 25), ('Whiteboard', 80),
    ]:
        if not env['product.template'].search([('name', '=', name)], limit=1):
            env['product.template'].create({'name': name, 'type': 'consu', 'list_price': price})
