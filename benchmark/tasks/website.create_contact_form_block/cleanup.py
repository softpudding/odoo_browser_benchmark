"""Clean up website.create_contact_form_block artifacts."""


def cleanup(env):
    env["website.rewrite"].search([("url_from", "=", "/talk-to-sales")]).unlink()
    env["website.page"].search([("url", "=", "/talk-to-sales")]).unlink()
