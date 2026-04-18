"""Cleanup for website.create_blog_post_publish."""


def cleanup(env):
    env["blog.post"].with_context(active_test=False).search([
        ("name", "=", "Product Launch Announcement"),
    ]).unlink()
