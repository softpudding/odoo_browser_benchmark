"""Clean up artifacts from previous runs."""


def cleanup(env):
    for name in ('Azure Interior', 'Deco Addict', 'Gemini Furniture'):
        partner = env['res.partner'].search([('name', '=', name)], limit=1)
        if partner:
            env['sale.order'].search([
                ('partner_id', '=', partner.id),
                ('state', '=', 'draft'),
            ]).unlink()
