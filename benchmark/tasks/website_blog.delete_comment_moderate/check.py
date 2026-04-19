"""Postcondition checks for website_blog.delete_comment_moderate.

Validates:
1. Exactly one blog.post named 'Bench Mod Post' exists, still published.
2. Post title, blog, author, body unchanged from seed.
3. The chatter on the post now holds exactly ONE visible comment
   (non-empty body, message_type='comment', subtype_id=mail.mt_comment,
   NOT inside the trash/internal buckets). That comment must be from
   'Reviewer Good' and contain the 'Great write-up' marker phrase.
4. The spam comment from 'Spam Bot' is gone from the chatter. The
   Odoo chatter Delete action wires through
   `/mail/message/update_content` with body='' — the mail.message
   record may either be unlinked OR linger with empty body. Both
   outcomes are accepted: the check requires that no non-empty spam
   body survives on the post.
5. No new top-level comments were posted by the agent (e.g. a
   'Spam removed' follow-up note would be flagged).
6. The Reviewer Good comment is still intact (body still contains
   the 'Great write-up' marker).
"""

import re


POST_NAME = "Bench Mod Post"
BLOG_NAME = "Bench News"
GOOD_LOGIN = "reviewer_good"
GOOD_NAME = "Reviewer Good"
SPAM_LOGIN = "spam_bot"
SPAM_MARKER = "BUY CHEAP"
GOOD_MARKER = "Great write-up"


def _plain(body):
    text = re.sub(r"<[^>]+>", " ", body or "")
    return " ".join(text.split()).strip()


def check(env):
    failures = []

    posts = env["blog.post"].with_context(active_test=False).search(
        [("name", "=", POST_NAME)],
    )
    if not posts:
        return [f"Blog post '{POST_NAME}' not found"]
    if len(posts) > 1:
        failures.append(
            f"Expected exactly 1 post named '{POST_NAME}', found {len(posts)}"
        )
    post = posts[:1]

    # --- Post identity / publication state unchanged -----------------------
    if not post.blog_id or post.blog_id.name != BLOG_NAME:
        failures.append(
            f"Blog is {post.blog_id.name!r}, expected {BLOG_NAME!r}"
        )
    if post.name != POST_NAME:
        failures.append(f"Post name is {post.name!r}, expected {POST_NAME!r}")
    if not post.is_published:
        failures.append(
            "Post was unpublished; is_published=True is required"
        )
    if not post.website_published:
        failures.append(
            "Post website_published is False; task must keep it published"
        )

    admin = env.ref("base.user_admin", raise_if_not_found=False)
    if admin and post.author_id and post.author_id.id != admin.partner_id.id:
        failures.append(
            f"Post author changed to {post.author_id.display_name!r}; "
            f"must remain admin ({admin.partner_id.display_name!r})"
        )
    if not post.content or "body of the Bench Mod Post" not in (post.content or ""):
        failures.append(
            "Post content appears modified — seeded marker phrase missing"
        )

    # --- Inspect chatter messages ------------------------------------------
    comment_subtype = env.ref("mail.mt_comment", raise_if_not_found=False)
    if not comment_subtype:
        return failures + ["mail.mt_comment subtype not found"]

    all_msgs = env["mail.message"].sudo().search([
        ("model", "=", "blog.post"),
        ("res_id", "=", post.id),
        ("message_type", "=", "comment"),
        ("subtype_id", "=", comment_subtype.id),
    ])

    # Visible (non-empty body) chatter comments after the moderation.
    visible = []
    for msg in all_msgs:
        text = _plain(msg.body)
        if text:
            visible.append(msg)

    # --- Spam must be gone (unlinked or body emptied) ----------------------
    lingering_spam = [
        m for m in all_msgs if SPAM_MARKER in _plain(m.body)
    ]
    if lingering_spam:
        failures.append(
            f"Spam comment is still present with body containing "
            f"{SPAM_MARKER!r} (expected unlinked or body cleared); "
            f"{len(lingering_spam)} offending message(s)."
        )

    # --- Good review must still be visible ---------------------------------
    good_messages = [
        m for m in all_msgs if GOOD_MARKER in _plain(m.body)
    ]
    if not good_messages:
        failures.append(
            f"Reviewer Good comment missing — no message with "
            f"{GOOD_MARKER!r} marker survives on the post."
        )
    else:
        good_user = env["res.users"].with_context(active_test=False).search(
            [("login", "=", GOOD_LOGIN)], limit=1,
        )
        if good_user and good_user.partner_id:
            if not any(m.author_id == good_user.partner_id for m in good_messages):
                failures.append(
                    "Reviewer Good comment author_id was changed — "
                    "no surviving good-review comment is authored by "
                    f"{GOOD_NAME!r}'s partner."
                )

    # --- Exactly one visible chatter comment on the post -------------------
    if len(visible) != 1:
        failures.append(
            f"Expected exactly 1 visible (non-empty) chatter comment on "
            f"the post after moderation, got {len(visible)}"
        )
    else:
        if GOOD_MARKER not in _plain(visible[0].body):
            failures.append(
                "The single remaining chatter comment is not the "
                "Reviewer Good review."
            )

    # --- No new admin-authored comment posted (agent must not reply/log) --
    if admin:
        admin_comments = [
            m for m in all_msgs
            if m.author_id == admin.partner_id and _plain(m.body)
        ]
        if admin_comments:
            failures.append(
                f"Admin posted {len(admin_comments)} extra chatter "
                f"comment(s); the task forbids replying or summarising."
            )

    return failures
