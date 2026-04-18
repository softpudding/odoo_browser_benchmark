"""Postcondition checks for website_blog.create_post_with_cta_seo_schedule.

Validates:
1. Exactly one blog.post named "Bench Releases Q2 Features" exists.
2. Its blog_id.name is "Bench News".
3. Its `content` HTML contains both the CTA label 'Learn More' AND an anchor
   tag whose href is '/shop'.
4. website_meta_title and website_meta_description are set to the required
   strings.
5. published_date, when rendered in the admin's local TZ, equals
   2026-05-20 09:00:00.
6. is_published / website_published are BOTH False (scheduled, not live).
"""

import re
from datetime import datetime


BLOG_NAME = "Bench News"
POST_NAME = "Bench Releases Q2 Features"
CTA_LABEL = "Learn More"
CTA_HREF = "/shop"
SEO_TITLE = "Q2 Releases - Bench"
SEO_DESCRIPTION = (
    "Read about our Q2 release highlights and what it means for customers."
)
EXPECTED_LOCAL = datetime(2026, 5, 20, 9, 0, 0)


def _admin_tz(env):
    import pytz

    admin = env["res.users"].search([("login", "=", "admin")], limit=1)
    tz_name = (admin.tz if admin else None) or env.user.tz or "UTC"
    try:
        return pytz.timezone(tz_name)
    except Exception:
        return pytz.UTC


def _has_cta_anchor(html: str) -> bool:
    """Return True iff `html` contains an <a ... href="/shop" ...>Learn More</a>
    pattern (attribute order + quoting tolerant)."""
    if not html:
        return False
    # Find every <a ...>inner</a>; check that at least one has the right
    # href AND encloses the CTA label text.
    pattern = re.compile(
        r"<a\b([^>]*)>(.*?)</a>", re.IGNORECASE | re.DOTALL,
    )
    for attrs, inner in pattern.findall(html):
        href_match = re.search(
            r"""href\s*=\s*['"]([^'"]+)['"]""", attrs, re.IGNORECASE,
        )
        if not href_match:
            continue
        if href_match.group(1).strip() != CTA_HREF:
            continue
        # Strip any nested tags from the label.
        label = re.sub(r"<[^>]+>", "", inner).strip()
        if CTA_LABEL.lower() in label.lower():
            return True
    return False


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

    # Blog
    if not post.blog_id or post.blog_id.name != BLOG_NAME:
        failures.append(
            f"Blog is {post.blog_id.name!r}, expected {BLOG_NAME!r}"
        )

    # CTA: content HTML must have an <a href="/shop">Learn More</a> pattern
    content = post.content or ""
    if not _has_cta_anchor(content):
        failures.append(
            "CTA button/link missing: expected an <a href='/shop'>Learn More</a> "
            f"pattern in post content, got: {content!r}"
        )

    # SEO fields
    if (post.website_meta_title or "").strip() != SEO_TITLE:
        failures.append(
            f"website_meta_title is {post.website_meta_title!r}, expected {SEO_TITLE!r}"
        )
    if (post.website_meta_description or "").strip() != SEO_DESCRIPTION:
        failures.append(
            "website_meta_description is "
            f"{post.website_meta_description!r}, expected {SEO_DESCRIPTION!r}"
        )

    # Must stay unpublished (scheduled)
    if post.is_published or post.website_published:
        failures.append(
            "Post must remain unpublished (scheduled); is_published="
            f"{post.is_published}, website_published={post.website_published}"
        )

    # Publishing date — published_date is the storage field (UTC Datetime),
    # post_date is its computed/inverse alias.
    tz = _admin_tz(env)
    actual_dt = post.published_date or post.post_date
    if not actual_dt:
        failures.append("Post Publishing date is empty; expected 2026-05-20 09:00:00")
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

    return failures
