"""Postcondition checks for website_blog.schedule_post_future_date_unpublish.

Validates:
  1. Exactly one blog.post named 'Bench Future Post' exists.
  2. Post still lives in blog 'Bench News'.
  3. is_published is False AND website_published is False (pill OFF).
  4. post_date / published_date == 2026-08-15 12:00:00 in admin's local TZ.
  5. Title, content unchanged from seed.
"""

from datetime import datetime


POST_NAME = "Bench Future Post"
BLOG_NAME = "Bench News"
EXPECTED_LOCAL = datetime(2026, 8, 15, 12, 0, 0)


def _admin_tz(env):
    import pytz

    admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    tz_name = (admin.tz if admin else None) or env.user.tz or "UTC"
    try:
        return pytz.timezone(tz_name)
    except Exception:
        return pytz.UTC


def check(env):
    import pytz

    failures = []

    posts = env["blog.post"].with_context(active_test=False).search(
        [("name", "=", POST_NAME)],
    )
    if not posts:
        return [f"Blog post '{POST_NAME}' not found"]
    if len(posts) > 1:
        failures.append(
            f"Expected exactly one post named '{POST_NAME}', found {len(posts)}"
        )
    post = posts[:1]

    # Blog unchanged
    if not post.blog_id or post.blog_id.name != BLOG_NAME:
        failures.append(
            f"Blog is {post.blog_id.name!r}, expected {BLOG_NAME!r}"
        )

    # Title unchanged
    if post.name != POST_NAME:
        failures.append(f"Post name is {post.name!r}, expected {POST_NAME!r}")

    # Must be unpublished
    if post.is_published:
        failures.append(
            f"Post is_published is {post.is_published!r}, expected False"
        )
    if post.website_published:
        failures.append(
            f"Post website_published is {post.website_published!r}, expected False"
        )

    # Publishing date — published_date is the storage field (UTC Datetime),
    # post_date is its computed/inverse alias.
    tz = _admin_tz(env)
    actual_dt = post.published_date or post.post_date
    if not actual_dt:
        failures.append(
            "Post Publishing date is empty; expected 2026-08-15 12:00:00"
        )
    else:
        if hasattr(actual_dt, "hour"):
            local_actual = (
                pytz.UTC.localize(actual_dt).astimezone(tz).replace(tzinfo=None)
            )
        else:
            local_actual = datetime(actual_dt.year, actual_dt.month, actual_dt.day)
        if local_actual != EXPECTED_LOCAL:
            failures.append(
                f"Publishing date (admin local) is {local_actual.isoformat()}, "
                f"expected {EXPECTED_LOCAL.isoformat()}"
            )

    # Content unchanged (seeded marker phrase present)
    if not post.content or "body of the Bench Future Post" not in (post.content or ""):
        failures.append(
            "Post content appears modified — seeded marker phrase missing"
        )

    return failures
