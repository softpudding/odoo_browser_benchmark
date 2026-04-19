"""Postcondition checks for website_blog.create_post_with_cta_seo_schedule.

Validates:
1. Exactly one blog.post named "Bench New Feature Launch" exists.
2. Its blog_id points to "Bench Tech Blog".
3. website_meta_title == "Bench New Feature".
4. website_meta_description == "Announcing our new bench feature".
5. The literal CTA string "Click here for details" appears in the
   post content (HTML body, case-insensitive match on the text).
6. published_date / post_date equals 2026-05-20 10:00:00 in the admin
   local timezone.
7. is_published and website_published are both False.
"""

from datetime import datetime


POST_NAME = "Bench New Feature Launch"
BLOG_NAME = "Bench Tech Blog"
EXPECTED_META_TITLE = "Bench New Feature"
EXPECTED_META_DESCRIPTION = "Announcing our new bench feature"
CTA_TEXT = "Click here for details"
EXPECTED_LOCAL = datetime(2026, 5, 20, 10, 0, 0)


def _admin_tz(env):
    import pytz
    admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    tz_name = (admin.tz if admin else None) or env.user.tz or "UTC"
    try:
        return pytz.timezone(tz_name)
    except Exception:
        return pytz.UTC


def _strip_html(raw):
    """Very small HTML-to-text fallback (no external deps)."""
    if not raw:
        return ""
    import re
    return re.sub(r"<[^>]+>", " ", raw)


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

    # Blog must be Bench Tech Blog
    if not post.blog_id or post.blog_id.name != BLOG_NAME:
        failures.append(
            f"Post blog is {post.blog_id.name!r}, expected {BLOG_NAME!r}"
        )

    # SEO title / description
    if (post.website_meta_title or "").strip() != EXPECTED_META_TITLE:
        failures.append(
            f"website_meta_title is {post.website_meta_title!r}, "
            f"expected {EXPECTED_META_TITLE!r}"
        )
    if (post.website_meta_description or "").strip() != EXPECTED_META_DESCRIPTION:
        failures.append(
            f"website_meta_description is {post.website_meta_description!r}, "
            f"expected {EXPECTED_META_DESCRIPTION!r}"
        )

    # CTA text must appear in content (ignore tags; match substring
    # case-insensitive on the visible text).
    content_text = _strip_html(post.content or "").lower()
    if CTA_TEXT.lower() not in content_text:
        failures.append(
            f"Post content does not contain the call-to-action "
            f"{CTA_TEXT!r}. Visible text was: {content_text[:200]!r}"
        )

    # Scheduled date: convert UTC -> admin local TZ and compare.
    tz = _admin_tz(env)
    actual_dt = post.published_date or post.post_date
    if not actual_dt:
        failures.append(
            "Post has no published_date; expected 2026-05-20 10:00:00"
        )
    else:
        if hasattr(actual_dt, "hour"):
            local_actual = (
                pytz.UTC.localize(actual_dt)
                .astimezone(tz)
                .replace(tzinfo=None)
            )
        else:
            local_actual = datetime(
                actual_dt.year, actual_dt.month, actual_dt.day
            )
        if local_actual != EXPECTED_LOCAL:
            failures.append(
                f"Post published_date (admin local) is "
                f"{local_actual.isoformat()}, "
                f"expected {EXPECTED_LOCAL.isoformat()}"
            )

    # Must NOT be published (scheduled only).
    if post.is_published or post.website_published:
        failures.append(
            "Post must remain unpublished (is_published="
            f"{post.is_published}, website_published={post.website_published})"
        )

    return failures
