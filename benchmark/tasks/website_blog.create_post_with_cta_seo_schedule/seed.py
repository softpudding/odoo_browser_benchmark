"""Seed for website_blog.create_post_with_cta_seo_schedule.

Category: deep_ui_interaction (MEDIUM).

The agent must create one new blog.post inside the seeded blog
"Bench Tech Blog" with:
  * title "Bench New Feature Launch",
  * a content body containing the literal call-to-action
    "Click here for details",
  * website_meta_title / website_meta_description filled via the
    Promote (Optimize SEO) dialog,
  * published_date = 2026-05-20 10:00:00 (admin local time),
  * is_published still False (scheduled, not yet published).

Seed state:
- Blog "Bench Tech Blog" exists (we create it if missing).
- Distractor blog "Bench Marketing Blog" exists so the agent must pick
  the right one from the Blog dropdown.
- No blog.post named "Bench New Feature Launch" exists (strictly cleaned
  up on every run).
"""


BLOG_NAME = "Bench Tech Blog"
DISTRACTOR_BLOG_NAME = "Bench Marketing Blog"
POST_NAME = "Bench New Feature Launch"


def setup(env):
    # --- Cleanup prior runs (must come first) ---
    env["blog.post"].with_context(active_test=False).search(
        [("name", "=", POST_NAME)],
    ).unlink()

    # --- Ensure target blog exists ---
    blog = env["blog.blog"].with_context(active_test=False).search(
        [("name", "=", BLOG_NAME)], limit=1,
    )
    if not blog:
        blog = env["blog.blog"].create({"name": BLOG_NAME})
    elif not blog.active:
        blog.active = True

    # --- Ensure distractor blog exists ---
    distractor = env["blog.blog"].with_context(active_test=False).search(
        [("name", "=", DISTRACTOR_BLOG_NAME)], limit=1,
    )
    if not distractor:
        env["blog.blog"].create({"name": DISTRACTOR_BLOG_NAME})
    elif not distractor.active:
        distractor.active = True
