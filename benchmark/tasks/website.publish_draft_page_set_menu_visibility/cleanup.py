"""Cleanup for website.publish_draft_page_set_menu_visibility."""


PAGE_URL = "/about-us"
PAGE_NAME = "About Us"
PAGE_KEY = "benchmark.about_us_draft_page"
DISTRACTOR_MENU_NAME = "About"


def cleanup(env):
    # Remove the agent-added menu (+ any stale seeded rows).
    env["website.menu"].with_context(active_test=False).search([
        "|",
        ("url", "=", PAGE_URL),
        "&",
        ("name", "=", PAGE_NAME),
        ("website_id", "!=", False),
    ]).unlink()

    # Remove the distractor 'About' menu so the seed is fully reversible.
    env["website.menu"].with_context(active_test=False).search([
        ("name", "=", DISTRACTOR_MENU_NAME),
    ]).unlink()

    # Remove the seeded page + its view + any redirect rewrite.
    env["website.rewrite"].search([("url_from", "=", PAGE_URL)]).unlink()
    env["website.page"].with_context(active_test=False).search([
        ("url", "=", PAGE_URL),
    ]).unlink()
    env["ir.ui.view"].search([("key", "=", PAGE_KEY)]).unlink()
