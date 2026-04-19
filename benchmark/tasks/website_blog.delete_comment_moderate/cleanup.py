"""Cleanup for website_blog.delete_comment_moderate."""


POST_NAME = "Bench Mod Post"
BLOG_NAME = "Bench News"
GOOD_LOGIN = "reviewer_good"
SPAM_LOGIN = "spam_bot"


def cleanup(env):
    # Unlink messages attached to the post, then the post itself.
    posts = env["blog.post"].with_context(active_test=False).search(
        [("name", "=", POST_NAME)],
    )
    if posts:
        env["mail.message"].sudo().search([
            ("model", "=", "blog.post"),
            ("res_id", "in", posts.ids),
        ]).unlink()
        posts.unlink()

    # The 'Bench News' blog is shared across multiple website_blog tasks
    # (change_author_republish_post, create_post_with_cta_seo_schedule,
    # etc.) — the seed is idempotent and will re-activate it if
    # someone else archives it. Do NOT unlink it here.
    _ = BLOG_NAME
    # Leave reviewer_good / spam_bot portal users around across runs;
    # removing them would orphan any surviving mail.message.author_id
    # references and force res.partner cascade churn.
    _ = GOOD_LOGIN
    _ = SPAM_LOGIN
