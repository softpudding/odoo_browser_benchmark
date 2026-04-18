"""Cleanup for website.duplicate_page_rename_unpublish."""


SOURCE_NAME = "Bench Source Page"
SOURCE_URL = "/bench-source-page"
DUPLICATE_NAME = "Bench Duplicate Page"
DUPLICATE_URL = "/bench-duplicate-page"


def cleanup(env):
    env["website.page"].with_context(active_test=False).search([
        "|", "|", "|",
        ("url", "=", SOURCE_URL),
        ("url", "=", DUPLICATE_URL),
        ("name", "=", SOURCE_NAME),
        ("name", "=", DUPLICATE_NAME),
    ]).unlink()
