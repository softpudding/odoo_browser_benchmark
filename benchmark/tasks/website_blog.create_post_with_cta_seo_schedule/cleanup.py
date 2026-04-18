"""Cleanup for website_blog.create_post_with_cta_seo_schedule."""


POST_NAME = "Quarterly Launch Playbook"


def cleanup(env):
    env["blog.post"].with_context(active_test=False).search([
        ("name", "=", POST_NAME),
    ]).unlink()
