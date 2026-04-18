"""Postcondition checks for website.duplicate_page_rename_unpublish.

Validates:
1. Original 'Bench Original' page still exists at '/bench-original' and is
   still published.
2. A new 'Bench Original Draft' page exists at '/bench-original-draft' and
   is NOT published.
3. Exactly one of each page exists (no accidental duplicates / deletions).
"""


ORIGINAL_NAME = "Bench Original"
ORIGINAL_URL = "/bench-original"
DRAFT_NAME = "Bench Original Draft"
DRAFT_URL = "/bench-original-draft"


def check(env):
    failures = []

    Page = env["website.page"].with_context(active_test=False)

    # --- Original page checks ---
    originals = Page.search([("url", "=", ORIGINAL_URL)])
    if not originals:
        failures.append(
            f"Original page missing at {ORIGINAL_URL!r} (expected name {ORIGINAL_NAME!r})"
        )
    elif len(originals) > 1:
        failures.append(
            f"Expected exactly 1 page at {ORIGINAL_URL!r}, got {len(originals)}"
        )
    else:
        original = originals[0]
        if original.name != ORIGINAL_NAME:
            failures.append(
                f"Original page name is {original.name!r}, expected {ORIGINAL_NAME!r}"
            )
        if not original.is_published:
            failures.append(
                f"Original page {ORIGINAL_URL!r} must remain published"
            )

    # --- Duplicated / renamed page checks ---
    drafts = Page.search([("url", "=", DRAFT_URL)])
    if not drafts:
        failures.append(
            f"Duplicated page missing at {DRAFT_URL!r} (expected name {DRAFT_NAME!r})"
        )
    elif len(drafts) > 1:
        failures.append(
            f"Expected exactly 1 page at {DRAFT_URL!r}, got {len(drafts)}"
        )
    else:
        draft = drafts[0]
        if draft.name != DRAFT_NAME:
            failures.append(
                f"Draft page name is {draft.name!r}, expected {DRAFT_NAME!r}"
            )
        if draft.is_published:
            failures.append(
                f"Draft page {DRAFT_URL!r} must NOT be published"
            )

    # --- No extra pages named like either target ---
    name_matches = Page.search([
        "|",
        ("name", "=", ORIGINAL_NAME),
        ("name", "=", DRAFT_NAME),
    ])
    # Expect exactly 2 (original + draft).
    if len(name_matches) != 2:
        failures.append(
            f"Expected exactly 2 pages named {ORIGINAL_NAME!r} or {DRAFT_NAME!r}, "
            f"got {len(name_matches)}"
        )

    return failures
