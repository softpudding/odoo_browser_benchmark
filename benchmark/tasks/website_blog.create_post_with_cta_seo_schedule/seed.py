"""Seed for website_blog.create_post_with_cta_seo_schedule.

Category: deep_ui_interaction (MEDIUM).

Creates the target blog 'Bench News' (empty, no posts) and makes sure no
prior post titled 'Bench Releases Q2 Features' exists. The agent must:

  * create a new blog.post in 'Bench News' with the exact title,
  * add a CTA button block in the body (label 'Learn More', href='/shop'),
  * open the Optimize SEO dialog and set Meta Title + Meta Description,
  * schedule the Publishing date to 2026-05-20 09:00 (in the admin TZ),
  * save without publishing.

The scheduled publishing date is IN THE FUTURE (relative to 2026-04-18),
so 'is_published'/'website_published' stay False even after save — the
post is queued, not live.
"""


BLOG_NAME = "Bench News"
POST_NAME = "Bench Releases Q2 Features"


def setup(env):
    # --- Cleanup prior runs (must come before recreating) ---
    env["blog.post"].with_context(active_test=False).search(
        [("name", "=", POST_NAME)],
    ).unlink()

    # --- Blog: ensure exactly one, active ---
    blog = env["blog.blog"].with_context(active_test=False).search(
        [("name", "=", BLOG_NAME)], limit=1,
    )
    if blog:
        if not blog.active:
            blog.active = True
    else:
        env["blog.blog"].create({"name": BLOG_NAME})
