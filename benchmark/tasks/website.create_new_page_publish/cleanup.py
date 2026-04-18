"""Cleanup for website.create_new_page_publish."""


PAGE_NAME = "Bench New Page"
PAGE_URL = "/bench-new-page"


def cleanup(env):
    env["website.page"].with_context(active_test=False).search([
        "|",
        ("url", "=", PAGE_URL),
        ("name", "=", PAGE_NAME),
    ]).unlink()
