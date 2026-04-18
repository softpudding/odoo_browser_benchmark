"""Cleanup for website.add_image_snippet_swap_source."""


PAGE_URL = "/bench-image-page"


def cleanup(env):
    env["website.rewrite"].search([
        ("url_from", "in", [PAGE_URL]),
    ]).unlink()
    env["website.page"].with_context(active_test=False).search([
        ("url", "=", PAGE_URL),
    ]).unlink()
