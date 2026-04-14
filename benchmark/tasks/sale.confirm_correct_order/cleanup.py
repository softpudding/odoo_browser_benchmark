"""Clean up artifacts from previous runs."""


def cleanup(env):
    partner = env['res.partner'].search([('name', '=', 'Gemini Furniture')], limit=1)
    if partner:
        # Remove all SOs — seed will recreate the two draft ones
        env['sale.order'].search([
            ('partner_id', '=', partner.id),
        ]).unlink()
