"""Cleanup for website_blog.create_post_with_cta_seo_schedule."""


BLOG_NAME = "Bench Tech Blog"
DISTRACTOR_BLOG_NAME = "Bench Marketing Blog"
POST_NAME = "Bench New Feature Launch"


def cleanup(env):
    env["blog.post"].with_context(active_test=False).search(
        [("name", "=", POST_NAME)],
    ).unlink()
    # Leave the blogs in place — they are pre-existing content that other
    # runs of the same task rely on. Deleting them would force seed.py to
    # recreate them every single run, which can race with concurrent tasks.
    _ = (BLOG_NAME, DISTRACTOR_BLOG_NAME)
