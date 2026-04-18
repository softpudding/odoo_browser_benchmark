"""Postcondition checks for website.duplicate_page_rename_unpublish.

Validates:
1. Original 'Bench Source Page' still exists at '/bench-source-page'.
2. A new 'Bench Duplicate Page' page exists at '/bench-duplicate-page' and
   is NOT published.
3. Exactly one of each page exists (no accidental duplicates / deletions).
"""


SOURCE_NAME = "Bench Source Page"
SOURCE_URL = "/bench-source-page"
DUPLICATE_NAME = "Bench Duplicate Page"
DUPLICATE_URL = "/bench-duplicate-page"


def check(env):
    failures = []

    Page = env["website.page"].with_context(active_test=False)

    # --- Source page checks ---
    sources = Page.search([("url", "=", SOURCE_URL)])
    if not sources:
        failures.append(
            f"Source page missing at {SOURCE_URL!r} (expected name {SOURCE_NAME!r})"
        )
    elif len(sources) > 1:
        failures.append(
            f"Expected exactly 1 page at {SOURCE_URL!r}, got {len(sources)}"
        )
    else:
        source = sources[0]
        if source.name != SOURCE_NAME:
            failures.append(
                f"Source page name is {source.name!r}, expected {SOURCE_NAME!r}"
            )

    # --- Duplicated / renamed page checks ---
    duplicates = Page.search([("url", "=", DUPLICATE_URL)])
    if not duplicates:
        failures.append(
            f"Duplicated page missing at {DUPLICATE_URL!r} (expected name {DUPLICATE_NAME!r})"
        )
    elif len(duplicates) > 1:
        failures.append(
            f"Expected exactly 1 page at {DUPLICATE_URL!r}, got {len(duplicates)}"
        )
    else:
        duplicate = duplicates[0]
        if duplicate.name != DUPLICATE_NAME:
            failures.append(
                f"Duplicate page name is {duplicate.name!r}, expected {DUPLICATE_NAME!r}"
            )
        if duplicate.is_published:
            failures.append(
                f"Duplicate page {DUPLICATE_URL!r} must NOT be published"
            )

    # --- No extra pages named like either target ---
    name_matches = Page.search([
        "|",
        ("name", "=", SOURCE_NAME),
        ("name", "=", DUPLICATE_NAME),
    ])
    # Expect exactly 2 (source + duplicate).
    if len(name_matches) != 2:
        failures.append(
            f"Expected exactly 2 pages named {SOURCE_NAME!r} or {DUPLICATE_NAME!r}, "
            f"got {len(name_matches)}"
        )

    return failures
