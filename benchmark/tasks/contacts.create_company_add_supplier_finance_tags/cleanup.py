"""Cleanup for contacts.create_company_add_supplier_finance_tags."""


def cleanup(env):
    env["res.partner"].search([
        ("name", "=", "Harborview Components"),
        ("is_company", "=", True),
    ]).unlink()
