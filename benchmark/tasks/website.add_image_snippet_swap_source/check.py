"""Postcondition checks for website.add_image_snippet_swap_source.

The agent must have inserted an Image snippet into `/bench-image-page` and
swapped its src to `/web/image/website.library_image_10`.  We verify via
the view's arch_db rather than the iframe DOM because the arch is the
authoritative, persisted state.
"""


PAGE_URL = "/bench-image-page"
PAGE_NAME = "Bench Image Page"
TARGET_SRC = "/web/image/website.library_image_10"


def check(env):
    failures = []

    page = env["website.page"].search(
        [("url", "=", PAGE_URL)], limit=1
    )
    if not page:
        return [
            f"Target page {PAGE_URL} is missing; it should have been "
            f"seeded and preserved by the agent."
        ]

    arch_db = page.view_id.arch_db or ""

    # The image src must match the requested library image exactly.
    if TARGET_SRC not in arch_db:
        failures.append(
            f"Expected an <img> with src={TARGET_SRC!r} in the page arch; "
            f"not found."
        )

    # There should be an <img> tag on the page (sanity).
    if "<img" not in arch_db:
        failures.append(
            "Expected at least one <img> tag in the page arch after adding "
            "the Image snippet."
        )

    # The seeded heading must not have been deleted.
    if "Our Image Showcase" not in arch_db:
        failures.append(
            "Seeded heading 'Our Image Showcase' is missing; the agent "
            "should have added the Image snippet alongside, not replaced "
            "the page content."
        )

    # Page URL and title should be unchanged.
    if page.name != PAGE_NAME:
        failures.append(
            f"Page name changed to {page.name!r}; expected {PAGE_NAME!r}."
        )
    if page.url != PAGE_URL:
        failures.append(
            f"Page URL changed to {page.url!r}; expected {PAGE_URL!r}."
        )

    # Page must stay published.
    if not page.is_published:
        failures.append("Page was unpublished; it must stay published.")

    return failures
