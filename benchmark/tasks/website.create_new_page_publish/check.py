"""Postcondition checks for website.create_new_page_publish.

Validates:
1. Exactly one website.page exists at '/bench-new-page' with name
   'Bench New Page' and is_published=True.
2. The page's view arch contains the heading text 'Welcome to Bench'.
"""


PAGE_NAME = "Bench New Page"
PAGE_URL = "/bench-new-page"
HEADING_TEXT = "Welcome to Bench"


def check(env):
    failures = []

    Page = env["website.page"].with_context(active_test=False)

    pages = Page.search([("url", "=", PAGE_URL)])
    if not pages:
        failures.append(
            f"Page missing at {PAGE_URL!r} (expected name {PAGE_NAME!r})"
        )
        return failures
    if len(pages) > 1:
        failures.append(
            f"Expected exactly 1 page at {PAGE_URL!r}, got {len(pages)}"
        )
        return failures

    page = pages[0]

    if page.name != PAGE_NAME:
        failures.append(
            f"Page name is {page.name!r}, expected {PAGE_NAME!r}"
        )

    if not page.is_published:
        failures.append(
            f"Page {PAGE_URL!r} must be published (is_published=True)"
        )

    # Arch / rendered view must contain the required heading text.
    view = page.view_id
    arch = (view.arch or "") if view else ""
    if HEADING_TEXT not in arch:
        failures.append(
            f"Page view arch does not contain heading text {HEADING_TEXT!r}"
        )

    return failures
