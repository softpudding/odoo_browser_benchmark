"""Seed for website_blog.create_blog_with_two_posts_archive_one.

Category: deep_ui_interaction (MEDIUM).

The agent must:
  * Create a brand-new blog 'Bench Insights' (no pre-seeded blog).
  * Create two blog.posts ('April Update' and 'March Notes') under that blog,
    BOTH published.
  * Then open 'March Notes' and archive it (active=False) without deleting it
    and without touching 'April Update'.

This seed only ensures a clean slate by removing any leftover state from
prior runs; it does NOT create the target blog or posts.
"""


BLOG_NAME = "Bench Insights"
POST_APRIL = "April Update"
POST_MARCH = "March Notes"


def setup(env):
    # Remove leftover posts from previous runs (active or archived)
    env["blog.post"].with_context(active_test=False).search([
        ("name", "in", [POST_APRIL, POST_MARCH]),
    ]).unlink()
    # Remove leftover blog from previous runs (active or archived)
    env["blog.blog"].with_context(active_test=False).search([
        ("name", "=", BLOG_NAME),
    ]).unlink()
