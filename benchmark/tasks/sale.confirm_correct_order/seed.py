"""Create four quotations — only one has BOTH Standing Desk AND Office Chair.

SO1: Standing Desk only — $450
SO2: Office Chair only — $450 (3x $150)
SO3: Standing Desk + Office Chair — $600 (THE ANSWER)
SO4: Large Desk + Whiteboard — $400
"""


def setup(env):
    partner = env['res.partner'].search([('name', '=', 'Gemini Furniture')], limit=1)
    if not partner:
        partner = env['res.partner'].create({'name': 'Gemini Furniture', 'email': 'gemini@example.com'})

    products = {}
    for name, price in [('Standing Desk', 450), ('Office Chair', 150),
                        ('Large Desk', 320), ('Whiteboard', 80)]:
        p = env['product.product'].search([('name', '=', name)], limit=1)
        if not p:
            t = env['product.template'].create({'name': name, 'type': 'consu', 'list_price': price})
            p = t.product_variant_id
        products[name] = p

    env['sale.order'].search([('partner_id', '=', partner.id)]).unlink()

    admin = env.ref('base.user_admin')

    def make_so(lines):
        so = env['sale.order'].create({'partner_id': partner.id, 'user_id': admin.id})
        for prod_name, qty, price in lines:
            env['sale.order.line'].create({
                'order_id': so.id,
                'product_id': products[prod_name].id,
                'product_uom_qty': qty,
                'price_unit': price,
            })
        return so

    # SO1: Standing Desk only
    make_so([('Standing Desk', 1, 450)])
    # SO2: Office Chair only (same total as SO1 — can't distinguish by amount!)
    make_so([('Office Chair', 3, 150)])
    # SO3: Standing Desk + Office Chair — THE ANSWER
    make_so([('Standing Desk', 1, 450), ('Office Chair', 1, 150)])
    # SO4: Large Desk + Whiteboard
    make_so([('Large Desk', 1, 320), ('Whiteboard', 1, 80)])
