"""Postcondition checks for website_blog.edit_post_change_author_add_tags_schedule.

Validates:
1. Exactly one blog.post named "Spring Planning Recap" exists.
2. Its author_id is the partner of user "alice.authoress" (Alice Authoress).
3. Its tag_ids contain BOTH "Planning" and "Quarterly".
4. Its tag_ids do NOT contain the distractor "Retrospective".
5. Its post_date (a Datetime, stored UTC) equals 2026-04-25 09:00:00 in the
   admin user's local timezone.
6. is_published / website_published remain False (post must NOT be published).
7. Title, blog, content unchanged from seed.
"""

from datetime import datetime


POST_NAME = "Spring Planning Recap"
BLOG_NAME = "Bench Engineering Blog"
ALICE_LOGIN = "alice.authoress"
ALICE_NAME = "Alice Authoress"
TAG_PLANNING = "Planning"
TAG_QUARTERLY = "Quarterly"
TAG_RETROSPECTIVE = "Retrospective"

EXPECTED_LOCAL = datetime(2026, 4, 25, 9, 0, 0)


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

    # Author must be Alice Authoress's partner
    alice_user = env["res.users"].with_context(active_test=False).search(
        [("login", "=", ALICE_LOGIN)], limit=1,
    )
    if not alice_user:
        failures.append(f"Seeded user '{ALICE_LOGIN}' not found")
    else:
        if not post.author_id:
            failures.append("Post has no author; expected Alice Authoress")
        elif post.author_id.id != alice_user.partner_id.id:
            failures.append(
                "Post author_id is "
                f"{post.author_id.display_name!r} (id={post.author_id.id}), "
                f"expected {ALICE_NAME!r} "
                f"(partner id={alice_user.partner_id.id})"
            )

    # Tags: both required, distractor forbidden
    tag_names = set(post.tag_ids.mapped("name"))
    if TAG_PLANNING not in tag_names:
        failures.append(
            f"Tag {TAG_PLANNING!r} missing; tags are {sorted(tag_names)!r}"
        )
    if TAG_QUARTERLY not in tag_names:
        failures.append(
            f"Tag {TAG_QUARTERLY!r} missing; tags are {sorted(tag_names)!r}"
        )
    if TAG_RETROSPECTIVE in tag_names:
        failures.append(
            f"Distractor tag {TAG_RETROSPECTIVE!r} must NOT be added; "
            f"tags are {sorted(tag_names)!r}"
        )

    # Publishing date — Datetime stored UTC, displayed in admin local TZ.
    tz = _admin_tz(env)
    actual_dt = post.post_date
    if not actual_dt:
        failures.append("Post post_date is empty; expected 2026-04-25 09:00:00")
    else:
        # post_date is a stored Datetime (UTC). Convert UTC -> admin local.
        if hasattr(actual_dt, "hour"):
            local_actual = pytz.UTC.localize(actual_dt).astimezone(tz).replace(tzinfo=None)
        else:
            # date-only fallback
            local_actual = datetime(actual_dt.year, actual_dt.month, actual_dt.day)
        if local_actual != EXPECTED_LOCAL:
            failures.append(
                f"Post post_date (admin local) is {local_actual.isoformat()}, "
                f"expected {EXPECTED_LOCAL.isoformat()}"
            )

    # Must NOT be published
    if post.is_published or post.website_published:
        failures.append(
            "Post must remain unpublished (is_published="
            f"{post.is_published}, website_published={post.website_published})"
        )

    # Content + title unchanged from seed
    if post.name != POST_NAME:
        failures.append(f"Post name is {post.name!r}, expected {POST_NAME!r}")
    if not post.content or "spring planning meeting" not in (post.content or "").lower():
        failures.append(
            "Post content appears modified — seeded marker phrase missing"
        )

    return failures
