"""Cleanup for website.set_page_seo_fields."""


def cleanup(env):
    env["website.page"].with_context(active_test=False).search([
        ("url", "=", "/bench-seo-page"),
    ]).unlink()
