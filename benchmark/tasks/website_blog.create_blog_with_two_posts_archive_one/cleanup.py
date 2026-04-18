"""Cleanup for website_blog.create_blog_with_two_posts_archive_one."""


BLOG_NAME = "Bench Insights"
POST_APRIL = "April Update"
POST_MARCH = "March Notes"


def cleanup(env):
    env["blog.post"].with_context(active_test=False).search([
        ("name", "in", [POST_APRIL, POST_MARCH]),
    ]).unlink()
    env["blog.blog"].with_context(active_test=False).search([
        ("name", "=", BLOG_NAME),
    ]).unlink()
