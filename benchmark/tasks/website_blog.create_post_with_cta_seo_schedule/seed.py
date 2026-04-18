"""Seed for website_blog.create_post_with_cta_seo_schedule."""


BLOG_NAME = "Bench Content Studio"
POST_NAME = "Quarterly Launch Playbook"


def setup(env):
    env["blog.post"].with_context(active_test=False).search([
        ("name", "=", POST_NAME),
    ]).unlink()

    blog = env["blog.blog"].with_context(active_test=False).search([
        ("name", "=", BLOG_NAME),
    ], limit=1)
    if blog:
        if not blog.active:
            blog.active = True
    else:
        env["blog.blog"].create({"name": BLOG_NAME})
