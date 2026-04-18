"""Cleanup for website_blog.edit_post_change_author_add_tags_schedule."""


POST_NAME = "Spring Planning Recap"
BLOG_NAME = "Bench Engineering Blog"
TAG_NAMES = ["Planning", "Quarterly", "Retrospective"]
USER_LOGINS = ["alice.authoress", "bob.blogger"]


def cleanup(env):
    env["blog.post"].with_context(active_test=False).search(
        [("name", "=", POST_NAME)],
    ).unlink()
    env["blog.tag"].search([("name", "in", TAG_NAMES)]).unlink()
    env["blog.blog"].with_context(active_test=False).search(
        [("name", "=", BLOG_NAME)],
    ).unlink()
    # Leave seeded users in place; recreating them on every run is expensive
    # and they have no side effects on the post check.
    _ = USER_LOGINS
