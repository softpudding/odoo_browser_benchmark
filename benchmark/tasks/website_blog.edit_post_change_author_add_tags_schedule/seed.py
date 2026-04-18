"""Seed for website_blog.edit_post_change_author_add_tags_schedule.

Category: deep_ui_interaction (MEDIUM).

Creates an existing blog and an existing blog post with admin as author and
no tags. The agent must:
  * change the Author to "Alice Authoress" (a Many2one to res.partner inside
    the secondary "Publishing Options" group),
  * add two existing tags ("Planning" and "Quarterly") via the
    many2many_tags chip widget — without picking the distractor tag
    "Retrospective",
  * set the Publishing date (post_date) to 2026-04-25 09:00:00.

We pre-seed two users (alice, bob — bob is a distractor) and three tags
(Planning, Quarterly, Retrospective — Retrospective is a distractor).
"""


BLOG_NAME = "Bench Engineering Blog"
POST_NAME = "Spring Planning Recap"
POST_CONTENT = (
    "<p>Notes from the spring planning meeting. "
    "Action items are tracked separately.</p>"
)

ALICE_LOGIN = "alice.authoress"
ALICE_NAME = "Alice Authoress"
ALICE_EMAIL = "alice.authoress@example.com"

BOB_LOGIN = "bob.blogger"
BOB_NAME = "Bob Blogger"
BOB_EMAIL = "bob.blogger@example.com"

TAG_PLANNING = "Planning"
TAG_QUARTERLY = "Quarterly"
TAG_RETROSPECTIVE = "Retrospective"  # distractor


def _ensure_user(env, login, name, email):
    """Create or update an internal user with deterministic credentials."""
    user = env["res.users"].with_context(active_test=False).search(
        [("login", "=", login)], limit=1,
    )
    if user:
        if not user.active:
            user.active = True
        user.write({"name": name, "email": email})
        if user.partner_id:
            user.partner_id.write({"name": name, "email": email})
        return user

    # Find a portal/internal group: keep it as a regular internal user.
    return env["res.users"].create({
        "login": login,
        "name": name,
        "email": email,
        "password": login,
    })


def setup(env):
    # --- Cleanup prior runs (must come before recreating) ---
    env["blog.post"].with_context(active_test=False).search(
        [("name", "=", POST_NAME)],
    ).unlink()

    # Detach tags from any post first by deleting them outright (they're
    # only used in this benchmark).
    env["blog.tag"].search(
        [("name", "in", [TAG_PLANNING, TAG_QUARTERLY, TAG_RETROSPECTIVE])],
    ).unlink()

    env["blog.blog"].with_context(active_test=False).search(
        [("name", "=", BLOG_NAME)],
    ).unlink()

    # --- Users (kept across runs to avoid orphan partners) ---
    alice = _ensure_user(env, ALICE_LOGIN, ALICE_NAME, ALICE_EMAIL)
    bob = _ensure_user(env, BOB_LOGIN, BOB_NAME, BOB_EMAIL)
    # Touch bob so linters don't complain — bob is a distractor partner
    # that should appear in the author dropdown but must NOT be picked.
    _ = bob

    # --- Blog ---
    blog = env["blog.blog"].create({"name": BLOG_NAME})

    # --- Tags (Planning, Quarterly are targets; Retrospective is distractor) ---
    env["blog.tag"].create([
        {"name": TAG_PLANNING},
        {"name": TAG_QUARTERLY},
        {"name": TAG_RETROSPECTIVE},
    ])

    # --- Post: admin author, no tags, NOT published, no post_date set ---
    admin = env.ref("base.user_admin")
    post = env["blog.post"].create({
        "name": POST_NAME,
        "blog_id": blog.id,
        "author_id": admin.partner_id.id,
        "tag_ids": [(6, 0, [])],
        "is_published": False,
        "website_published": False,
        "content": POST_CONTENT,
    })
    # Force the post_date to a clear, OLD value so the agent's change to
    # 2026-04-25 09:00:00 is unambiguous. published_date is the underlying
    # writable Datetime; post_date is computed/inverse from it.
    post.write({"published_date": False})
    # Ensure not auto-published by stray writes.
    post.write({"is_published": False, "website_published": False})

    _ = alice  # silence linter
