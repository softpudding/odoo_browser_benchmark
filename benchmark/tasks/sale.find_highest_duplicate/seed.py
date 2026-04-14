"""Seed quotations requiring cross-referencing confirmed vs draft orders.

The agent must:
1. Sum confirmed order values per customer
2. Find customer with highest confirmed total → Azure ($1600 confirmed)
3. Among Azure's drafts, find the lowest → $280
4. Duplicate it

Azure:  confirmed=$1600 (highest!), drafts=$960, $280 (lowest=answer)
Deco:   confirmed=$1400,            drafts=$750, $500
Gemini: confirmed=$900,             drafts=$1100, $400
"""


def setup(env):
    partners = {}
    for name, email in [('Azure Interior', 'azure@example.com'),
                        ('Deco Addict', 'deco@example.com'),
                        ('Gemini Furniture', 'gemini@example.com')]:
        p = env['res.partner'].search([('name', '=', name)], limit=1)
        if not p:
            p = env['res.partner'].create({'name': name, 'email': email})
        partners[name] = p

    products = {}
    for name, price in [('Large Desk', 320), ('Office Chair', 150),
                        ('Standing Desk', 450), ('Whiteboard', 80),
                        ('Monitor Arm', 75), ('Desk Lamp', 60)]:
        p = env['product.product'].search([('name', '=', name)], limit=1)
        if not p:
            t = env['product.template'].create({'name': name, 'type': 'consu', 'list_price': price})
            p = t.product_variant_id
        products[name] = p

    # Clean all SOs for these partners
    for partner in partners.values():
        env['sale.order'].search([('partner_id', '=', partner.id)]).unlink()

    admin = env.ref('base.user_admin')

    def make_so(partner, lines, confirm=False):
        so = env['sale.order'].create({'partner_id': partner.id, 'user_id': admin.id})
        for prod_name, qty, price in lines:
            env['sale.order.line'].create({
                'order_id': so.id,
                'product_id': products[prod_name].id,
                'product_uom_qty': qty,
                'price_unit': price,
            })
        if confirm:
            so.action_confirm()
        return so

    # Azure: confirmed total = $1600 (highest!)
    make_so(partners['Azure Interior'], [('Large Desk', 2, 320), ('Standing Desk', 1, 450)], confirm=True)   # $1090 confirmed
    make_so(partners['Azure Interior'], [('Office Chair', 3, 150), ('Desk Lamp', 1, 60)], confirm=True)      # $510 confirmed
    # Azure drafts
    make_so(partners['Azure Interior'], [('Large Desk', 3, 320)])       # $960 draft
    make_so(partners['Azure Interior'], [('Monitor Arm', 2, 75), ('Whiteboard', 1, 80), ('Desk Lamp', 1, 50)])  # $280 draft ← ANSWER

    # Deco: confirmed total = $1400
    make_so(partners['Deco Addict'], [('Standing Desk', 2, 450), ('Office Chair', 2, 150)], confirm=True)    # $1200 confirmed
    make_so(partners['Deco Addict'], [('Whiteboard', 2, 80), ('Desk Lamp', 1, 40)], confirm=True)            # $200 confirmed
    # Deco drafts
    make_so(partners['Deco Addict'], [('Office Chair', 5, 150)])        # $750 draft
    make_so(partners['Deco Addict'], [('Standing Desk', 1, 450), ('Desk Lamp', 1, 50)])  # $500 draft

    # Gemini: confirmed total = $900
    make_so(partners['Gemini Furniture'], [('Standing Desk', 2, 450)], confirm=True)     # $900 confirmed
    # Gemini drafts
    make_so(partners['Gemini Furniture'], [('Large Desk', 3, 320), ('Monitor Arm', 2, 75)])  # $1110 draft
    make_so(partners['Gemini Furniture'], [('Office Chair', 2, 150), ('Whiteboard', 1, 80), ('Desk Lamp', 1, 20)])  # $400 draft
