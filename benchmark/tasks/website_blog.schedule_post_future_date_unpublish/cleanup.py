"""Cleanup for website_blog.schedule_post_future_date_unpublish."""


POST_NAME = "Bench Future Post"
BLOG_NAME = "Bench News"


def cleanup(env):
    env["blog.post"].with_context(active_test=False).search(
        [("name", "=", POST_NAME)],
    ).unlink()
    # Shared blog; do NOT unlink — other website_blog tasks re-use it.
    _ = BLOG_NAME
