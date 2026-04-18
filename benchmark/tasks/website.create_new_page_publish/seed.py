"""Seed for website.create_new_page_publish.

Category: deep_ui_interaction (MEDIUM).

Starting state: no website.page exists at '/bench-new-page'. The agent must
open the Website app, create a new blank page named 'Bench New Page' at
'/bench-new-page', add an H1 heading 'Welcome to Bench', and publish it.

This seed only removes any leftover 'Bench New Page' / '/bench-new-page'
pages from prior runs so it is idempotent. No new page is created — that is
the agent's job.
"""


PAGE_NAME = "Bench New Page"
PAGE_URL = "/bench-new-page"


def setup(env):
    # Idempotent cleanup of any previous run's artifacts.
    env["website.page"].with_context(active_test=False).search([
        "|",
        ("url", "=", PAGE_URL),
        ("name", "=", PAGE_NAME),
    ]).unlink()
