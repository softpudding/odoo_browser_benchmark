"""Postcondition checks for website_blog.create_blog_with_two_posts_archive_one.

Validates:
1. A blog.blog named 'Bench Insights' exists.
2. Exactly one blog.post named 'April Update' exists, active=True, published=True,
   and belongs to the 'Bench Insights' blog.
3. Exactly one blog.post named 'March Notes' exists (search with active_test=False
   so we can find archived records), active=False, AND not deleted.
4. 'March Notes' belongs to the 'Bench Insights' blog (or, defensively, accept
   that it remains in whatever blog the agent placed it — but the prompt says
   Bench Insights, so we enforce it).
"""


BLOG_NAME = "Bench Insights"
POST_APRIL = "April Update"
POST_MARCH = "March Notes"


def check(env):
    failures = []

    blog = env["blog.blog"].with_context(active_test=False).search(
        [("name", "=", BLOG_NAME)], limit=2,
    )
    if not blog:
        return [f"Blog {BLOG_NAME!r} not found"]
    if len(blog) > 1:
        failures.append(
            f"Expected exactly one blog named {BLOG_NAME!r}, found {len(blog)}"
        )
    blog = blog[:1]
    if not blog.active:
        failures.append(f"Blog {BLOG_NAME!r} is archived; expected active=True")

    # April Update — active and published
    april_all = env["blog.post"].with_context(active_test=False).search(
        [("name", "=", POST_APRIL)],
    )
    if not april_all:
        failures.append(f"Blog post {POST_APRIL!r} not found")
    elif len(april_all) > 1:
        failures.append(
            f"Expected exactly one post named {POST_APRIL!r}, found {len(april_all)}"
        )
    else:
        april = april_all
        if not april.active:
            failures.append(
                f"Post {POST_APRIL!r} must be Active (active=True); is archived"
            )
        if not april.is_published:
            failures.append(
                f"Post {POST_APRIL!r} must be Published; is_published=False"
            )
        if not april.blog_id or april.blog_id.id != blog.id:
            failures.append(
                f"Post {POST_APRIL!r} blog is "
                f"{april.blog_id.name!r}, expected {BLOG_NAME!r}"
            )

    # March Notes — must exist as an ARCHIVED record
    march_all = env["blog.post"].with_context(active_test=False).search(
        [("name", "=", POST_MARCH)],
    )
    if not march_all:
        failures.append(
            f"Blog post {POST_MARCH!r} not found — must remain in DB (archived, "
            f"not deleted)"
        )
    elif len(march_all) > 1:
        failures.append(
            f"Expected exactly one post named {POST_MARCH!r}, found {len(march_all)}"
        )
    else:
        march = march_all
        if march.active:
            failures.append(
                f"Post {POST_MARCH!r} must be Archived (active=False); active=True"
            )
        # When archived, Odoo's website auto-publish guard usually flips
        # is_published off. Still assert it.
        if march.is_published:
            failures.append(
                f"Post {POST_MARCH!r} must NOT be published once archived"
            )
        if not march.blog_id or march.blog_id.id != blog.id:
            failures.append(
                f"Post {POST_MARCH!r} blog is "
                f"{march.blog_id.name!r}, expected {BLOG_NAME!r}"
            )

    # Sanity: total of exactly two posts under this blog (no extras)
    blog_posts = env["blog.post"].with_context(active_test=False).search(
        [("blog_id", "=", blog.id)],
    )
    if len(blog_posts) != 2:
        names = sorted(blog_posts.mapped("name"))
        failures.append(
            f"Expected exactly 2 posts under blog {BLOG_NAME!r}, found "
            f"{len(blog_posts)}: {names!r}"
        )

    return failures
