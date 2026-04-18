"""Postcondition checks for website_blog.create_post_with_cta_seo_schedule."""

from datetime import datetime

from odoo.tools import html2plaintext


BLOG_NAME = "Bench Content Studio"
POST_NAME = "Quarterly Launch Playbook"
SUBTITLE = "Prepare your team before release day."
CTA_TEXT = "Download the launch checklist now."
SEO_TITLE = "Quarterly Launch Playbook | Bench Content"
SEO_DESCRIPTION = "Download the launch checklist and prepare your release team."
EXPECTED_LOCAL = datetime(2026, 6, 15, 10, 30, 0)


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

    posts = env["blog.post"].with_context(active_test=False).search([
        ("name", "=", POST_NAME),
    ])
    if not posts:
        return [f"Blog post '{POST_NAME}' not found"]
    if len(posts) > 1:
        failures.append(
            f"Expected exactly one post named '{POST_NAME}', found {len(posts)}"
        )
    post = posts[:1]

    if not post.blog_id or post.blog_id.name != BLOG_NAME:
        failures.append(
            f"Blog is {post.blog_id.name!r}, expected {BLOG_NAME!r}"
        )
    if (post.subtitle or "").strip() != SUBTITLE:
        failures.append(
            f"Subtitle is {post.subtitle!r}, expected {SUBTITLE!r}"
        )

    content_text = html2plaintext(post.content or "")
    if CTA_TEXT not in content_text:
        failures.append(
            f"CTA text {CTA_TEXT!r} not found in the post body"
        )

    if (post.website_meta_title or "").strip() != SEO_TITLE:
        failures.append(
            f"SEO title is {post.website_meta_title!r}, expected {SEO_TITLE!r}"
        )
    if (post.website_meta_description or "").strip() != SEO_DESCRIPTION:
        failures.append(
            "SEO description is "
            f"{post.website_meta_description!r}, expected {SEO_DESCRIPTION!r}"
        )

    if post.is_published or post.website_published:
        failures.append("Post must remain unpublished")

    tz = _admin_tz(env)
    actual_dt = post.post_date
    if not actual_dt:
        failures.append("Post publishing date is empty")
    else:
        local_actual = pytz.UTC.localize(actual_dt).astimezone(tz).replace(tzinfo=None)
        if local_actual != EXPECTED_LOCAL:
            failures.append(
                f"Publishing date (admin local) is {local_actual.isoformat()}, "
                f"expected {EXPECTED_LOCAL.isoformat()}"
            )

    return failures
