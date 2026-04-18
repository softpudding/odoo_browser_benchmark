"""Cleanup for website.set_page_seo_fields."""


def cleanup(env):
    env["website.page"].search([("url", "=", "/bench-product")]).unlink()
