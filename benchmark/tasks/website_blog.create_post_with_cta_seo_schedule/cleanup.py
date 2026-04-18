"""Cleanup for website_blog.create_post_with_cta_seo_schedule."""


BLOG_NAME = "Bench News"
POST_NAME = "Bench Releases Q2 Features"


def cleanup(env):
    env["blog.post"].with_context(active_test=False).search(
        [("name", "=", POST_NAME)],
    ).unlink()
    # Leave the blog in place; seed re-uses it. We only remove it if the
    # test run created a duplicate blog by mistake (defensive).
    blogs = env["blog.blog"].with_context(active_test=False).search(
        [("name", "=", BLOG_NAME)],
    )
    if len(blogs) > 1:
        blogs[1:].unlink()
