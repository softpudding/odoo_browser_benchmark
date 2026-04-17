"""Cleanup for website_blog.create_post_with_cover_tag_publish."""


def cleanup(env):
    env["blog.post"].with_context(active_test=False).search([
        ("name", "=", "Harbor Notes Rollout"),
    ]).unlink()
    env["blog.tag"].search([("name", "=", "Operations Spotlight")]).unlink()
    env["blog.blog"].with_context(active_test=False).search([
        ("name", "=", "Harbor Newsroom"),
    ]).unlink()
