"""Clean up artifacts from previous runs."""


def cleanup(env):
    partner = env['res.partner'].search([('name', '=', 'Deco Addict')], limit=1)
    if partner:
        env['sale.order'].search([
            ('partner_id', '=', partner.id),
            ('state', '=', 'draft'),
        ]).unlink()
