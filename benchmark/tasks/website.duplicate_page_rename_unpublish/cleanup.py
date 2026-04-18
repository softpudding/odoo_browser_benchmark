"""Cleanup for website.duplicate_page_rename_unpublish."""


ORIGINAL_NAME = "Bench Original"
ORIGINAL_URL = "/bench-original"
DRAFT_NAME = "Bench Original Draft"
DRAFT_URL = "/bench-original-draft"


def cleanup(env):
    env["website.page"].with_context(active_test=False).search([
        "|", "|", "|",
        ("url", "=", ORIGINAL_URL),
        ("url", "=", DRAFT_URL),
        ("name", "=", ORIGINAL_NAME),
        ("name", "=", DRAFT_NAME),
    ]).unlink()
