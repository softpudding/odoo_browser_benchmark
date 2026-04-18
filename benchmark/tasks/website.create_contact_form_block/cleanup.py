"""Cleanup for website.create_contact_form_block."""


PAGE_URL = "/bench-contact-form"


def cleanup(env):
    env["website.rewrite"].search([
        ("url_from", "in", [PAGE_URL]),
    ]).unlink()
    env["website.page"].with_context(active_test=False).search([
        ("url", "=", PAGE_URL),
    ]).unlink()
