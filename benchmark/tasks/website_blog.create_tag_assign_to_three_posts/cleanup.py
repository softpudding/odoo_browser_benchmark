"""Cleanup for website_blog.create_tag_assign_to_three_posts."""


BLOG_NAME = "Harbor Quarterly"
TAG_NAME = "Q2-2026"
POST_NAMES = ["Post-A", "Post-B", "Post-C", "Post-D"]


def cleanup(env):
    env["blog.post"].with_context(active_test=False).search(
        [("name", "in", POST_NAMES)],
    ).unlink()
    env["blog.tag"].search([("name", "=", TAG_NAME)]).unlink()
    env["blog.blog"].with_context(active_test=False).search(
        [("name", "=", BLOG_NAME)],
    ).unlink()
