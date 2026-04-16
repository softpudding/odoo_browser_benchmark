"""Cleanup for contacts.create_company_add_supplier_tag."""


def cleanup(env):
    env["res.partner"].search([("name", "=", "North Coast Fabrication")]).unlink()
