"""Postcondition checks for website.add_image_carousel_to_homepage.

The agent must have inserted an Image Gallery (carousel) snippet into
`/bench-gallery-test`.  We verify via the view's arch_db rather than
the iframe DOM because the arch is the authoritative, persisted state.
"""


def check(env):
    failures = []

    page = env["website.page"].search(
        [("url", "=", "/bench-gallery-test")], limit=1
    )
    if not page:
        return [
            "Target page /bench-gallery-test is missing; it should have been "
            "seeded and preserved by the agent."
        ]

    arch_db = page.view_id.arch_db or ""

    # Check the snippet block is present.  The Image Gallery snippet
    # uses the `s_image_gallery` wrapper class (also used by the Images
    # Wall variant).  Either `.s_image_gallery` or `.carousel`/`.s_carousel`
    # is acceptable — both mean "the agent successfully dropped a
    # gallery-family snippet".
    gallery_markers = ("s_image_gallery", "s_carousel", "carousel")
    if not any(m in arch_db for m in gallery_markers):
        failures.append(
            "Expected an image gallery / carousel block on the page; "
            "arch_db does not contain s_image_gallery, s_carousel, or "
            "carousel."
        )

    # Check at least 3 <img> tags are present in the page arch.
    img_count = arch_db.count("<img")
    if img_count < 3:
        failures.append(
            f"Expected at least 3 <img> children in the gallery block; "
            f"arch_db contains only {img_count}."
        )

    # The seeded heading should not have been deleted.
    if "Our Portfolio" not in arch_db:
        failures.append(
            "Seeded heading 'Our Portfolio' is missing; the agent should "
            "have added the gallery alongside, not replaced the page."
        )

    # Page URL and title should be unchanged.
    if page.name != "Bench Gallery Test":
        failures.append(
            f"Page title changed to {page.name!r}; expected 'Bench Gallery Test'."
        )
    if page.url != "/bench-gallery-test":
        failures.append(
            f"Page URL changed to {page.url!r}; expected '/bench-gallery-test'."
        )

    return failures
