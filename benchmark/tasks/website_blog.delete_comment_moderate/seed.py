"""Seed for website_blog.delete_comment_moderate.

Category: deep_ui_interaction (HARD).

Creates:
  * Blog 'Bench News' (shared idempotent blog across website_blog tasks;
    never unlinked in cleanup — seed re-activates if archived).
  * A single published blog.post 'Bench Mod Post' authored by admin.
  * Two portal users 'Reviewer Good' and 'Spam Bot' to sit as the
    author_id on two mail.message comments posted against the post's
    chatter. Both messages are message_type='comment' and
    subtype_id=mail.mt_comment, so they render as customer-facing
    'Send message' entries in the chatter (not internal Log notes).

Agent (admin) must open the post's backend chatter and use the
per-message Delete action (fa-trash icon behind the message
action-list overflow menu) to remove ONLY the Spam Bot comment,
leaving the Reviewer Good comment untouched.

## Why this is hard

- The chatter's Delete action is NOT surfaced as a top-level icon: it
  is behind a per-message hover toolbar whose trash icon only appears
  when the message is hovered, and on narrower viewports the
  trash/Delete item collapses into an overflow `...` "Expand" menu.
  Browser agents frequently either (a) click the wrong comment, (b)
  click Edit instead of Delete, or (c) cannot find the trash icon
  because it only exists on hover.
- A confirmation dialog ("Are you sure you want to bid farewell to
  this message forever?") must be dismissed with a primary-action
  click — agents that mis-click the cancel button see a silent no-op.
- The chatter displays TWO comments with similar layouts; only the
  comment whose author is 'Spam Bot' should be deleted. Deleting the
  wrong one fails both the "spam removed" AND "good review intact"
  postcondition gates.
"""


BLOG_NAME = "Bench News"
POST_NAME = "Bench Mod Post"
POST_CONTENT = (
    "<p>This is the body of the Bench Mod Post. The chatter below "
    "carries two public comments — one legitimate review and one "
    "spam message. Only the spam should be removed.</p>"
)

GOOD_LOGIN = "reviewer_good"
GOOD_NAME = "Reviewer Good"
GOOD_EMAIL = "reviewer.good@example.com"
GOOD_COMMENT = (
    "<p>Great write-up — the install walk-through is exactly what I "
    "needed. Keep these coming.</p>"
)

SPAM_LOGIN = "spam_bot"
SPAM_NAME = "Spam Bot"
SPAM_EMAIL = "spam.bot@example.com"
SPAM_COMMENT = (
    "<p>BUY CHEAP WATCHES NOW!!! Visit http://scam.example.com and "
    "get 90% off today only!!!</p>"
)


def _ensure_portal_user(env, login, name, email):
    """Create or refresh a portal-group user keyed by login.

    Keeps the same res.partner across runs (unlink would orphan any
    existing mail.message rows via author_id foreign key).
    """
    user = env["res.users"].with_context(active_test=False).search(
        [("login", "=", login)], limit=1,
    )
    group_portal = env.ref("base.group_portal")
    if user:
        if not user.active:
            user.active = True
        user.write({"name": name, "email": email})
        if user.partner_id:
            user.partner_id.write({"name": name, "email": email})
        if group_portal.id not in user.group_ids.ids:
            user.write({"group_ids": [(4, group_portal.id)]})
        return user
    return env["res.users"].create({
        "login": login,
        "name": name,
        "email": email,
        "password": login,
        "group_ids": [(6, 0, [group_portal.id])],
    })


def setup(env):
    # --- Cleanup prior runs -------------------------------------------------
    # Delete any prior 'Bench Mod Post' along with its attached messages
    # via cascade on mail.message(model=blog.post, res_id=post.id).
    prior = env["blog.post"].with_context(active_test=False).search(
        [("name", "=", POST_NAME)],
    )
    if prior:
        env["mail.message"].sudo().search([
            ("model", "=", "blog.post"),
            ("res_id", "in", prior.ids),
        ]).unlink()
        prior.unlink()

    # --- Blog: ensure 'Bench News' exists and is active ---------------------
    blog = env["blog.blog"].with_context(active_test=False).search(
        [("name", "=", BLOG_NAME)], limit=1,
    )
    if blog:
        if not blog.active:
            blog.active = True
    else:
        blog = env["blog.blog"].create({"name": BLOG_NAME})

    # --- Portal users -------------------------------------------------------
    good_user = _ensure_portal_user(env, GOOD_LOGIN, GOOD_NAME, GOOD_EMAIL)
    spam_user = _ensure_portal_user(env, SPAM_LOGIN, SPAM_NAME, SPAM_EMAIL)

    # --- Post: published, admin author --------------------------------------
    admin = env.ref("base.user_admin")
    post = env["blog.post"].create({
        "name": POST_NAME,
        "blog_id": blog.id,
        "author_id": admin.partner_id.id,
        "content": POST_CONTENT,
        "is_published": True,
        "website_published": True,
    })
    if not post.is_published or not post.website_published:
        post.write({"is_published": True, "website_published": True})

    # --- Seed the two chatter comments --------------------------------------
    # Use sudo().message_post() with subtype_xmlid='mail.mt_comment' so
    # the messages land on the chatter as public comments (NOT log
    # notes). author_id is set explicitly so the chatter renders
    # "Reviewer Good" and "Spam Bot" as the author display names.
    post.with_user(admin).sudo().message_post(
        body=GOOD_COMMENT,
        author_id=good_user.partner_id.id,
        message_type="comment",
        subtype_xmlid="mail.mt_comment",
    )
    post.with_user(admin).sudo().message_post(
        body=SPAM_COMMENT,
        author_id=spam_user.partner_id.id,
        message_type="comment",
        subtype_xmlid="mail.mt_comment",
    )

    # --- Sanity: exactly 2 comment messages present ------------------------
    comment_subtype = env.ref("mail.mt_comment")
    msgs = env["mail.message"].sudo().search([
        ("model", "=", "blog.post"),
        ("res_id", "=", post.id),
        ("message_type", "=", "comment"),
        ("subtype_id", "=", comment_subtype.id),
    ])
    if len(msgs) != 2:
        raise RuntimeError(
            "Seed expected 2 chatter comments on the post, got %d" % len(msgs)
        )
