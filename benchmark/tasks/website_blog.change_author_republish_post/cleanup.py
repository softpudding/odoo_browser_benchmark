"""Cleanup for website_blog.change_author_republish_post."""


POST_NAME = "Bench Blog Post"
BLOG_NAME = "Bench News"
EDITOR_LOGIN = "bench_editor"


def cleanup(env):
    env["blog.post"].with_context(active_test=False).search(
        [("name", "=", POST_NAME)],
    ).unlink()
    # The 'Bench News' blog is shared with other website_blog tasks
    # (create_post_with_cta_seo_schedule, etc.) — do NOT unlink it, the
    # seed is idempotent and will re-activate it if needed.
    # Leave the 'bench_editor' user in place across runs to avoid orphan
    # partners; it has no side effects once the post is re-seeded.
    _ = BLOG_NAME
    _ = EDITOR_LOGIN
