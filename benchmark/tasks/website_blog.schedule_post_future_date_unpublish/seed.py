"""Seed for website_blog.schedule_post_future_date_unpublish.

Category: deep_ui_interaction (HARD, tier 3).

Starting state:
- Blog 'Bench News' exists (created or re-used across website_blog tasks).
- A single *published* blog post 'Bench Future Post' lives in 'Bench News':
    * is_published = True
    * website_published = True
    * published_date / post_date = today (UTC now)
    * content = short body paragraph
    * author = admin's partner

The agent must:
  1. Open the post on the backend form.
  2. Toggle the Published pill OFF (unpublish: flips both is_published and
     website_published to False via website.published.mixin).
  3. Change the Publishing date (post_date, which is an inverse alias for
     published_date) to 2026-08-15 12:00:00 (admin local TZ).
  4. Save.

Hard-tier pattern:
  * Non-default publish-pill toggle (widget="website_publish_button"
    renders as a Bootstrap pill that BU often fails to flip cleanly).
  * Datetime widget on post_date (fragile Owl re-render — button-vs-input
    swap, see cookbook reference from create_post_with_cta_seo_schedule).
  * Two distinct surfaces on the same save action (toggle + datetime),
    either of which can be silently no-op'd by the agent.
"""

from datetime import datetime


BLOG_NAME = "Bench News"
POST_NAME = "Bench Future Post"
POST_CONTENT = (
    "<p>This is the body of the Bench Future Post. "
    "Only the Published toggle and Publishing date should change.</p>"
)


def setup(env):
    # --- Cleanup prior runs (must come before recreating) ---
    env["blog.post"].with_context(active_test=False).search(
        [("name", "=", POST_NAME)],
    ).unlink()

    # --- Blog: ensure exactly one active 'Bench News' blog ---
    blog = env["blog.blog"].with_context(active_test=False).search(
        [("name", "=", BLOG_NAME)], limit=1,
    )
    if blog:
        if not blog.active:
            blog.active = True
    else:
        blog = env["blog.blog"].create({"name": BLOG_NAME})

    # --- Post: published NOW with current datetime as published_date ---
    admin = env.ref("base.user_admin")
    now_utc = datetime.utcnow().replace(microsecond=0)

    post = env["blog.post"].create({
        "name": POST_NAME,
        "blog_id": blog.id,
        "author_id": admin.partner_id.id,
        "content": POST_CONTENT,
        "is_published": True,
        "website_published": True,
        "published_date": now_utc,
    })
    # Guarantee both flags are True (belt-and-braces: `create()` may bypass
    # the website.published.mixin inverse when `is_published` is the only
    # explicit setter on some variants).
    if not post.is_published or not post.website_published:
        post.write({"is_published": True, "website_published": True})
    if not post.published_date:
        post.write({"published_date": now_utc})
