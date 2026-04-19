"""Seed for website_blog.change_author_republish_post.

Category: deep_ui_interaction (MEDIUM).

Starting state:
- Blog 'Bench News' exists (created or re-used if still around from another
  task run).
- A published blog post 'Bench Blog Post' lives in 'Bench News', authored
  by admin (author_id = admin.partner_id), with a short body content.
- A second internal user 'Bench Editor' (login 'bench_editor', groups
  'base.group_user') is available so its linked res.partner is selectable
  in the Author m2o dropdown.

Agent must change the post's Author many2one from admin to 'Bench Editor'
while keeping the post published (is_published / website_published stay
True).
"""


BLOG_NAME = "Bench News"
POST_NAME = "Bench Blog Post"
POST_CONTENT = (
    "<p>This is the body of the Bench Blog Post. "
    "Only the Author should change — the rest of the post stays the same.</p>"
)

EDITOR_LOGIN = "bench_editor"
EDITOR_NAME = "Bench Editor"
EDITOR_EMAIL = "bench.editor@example.com"


def _ensure_editor(env):
    """Create or refresh the Bench Editor internal user."""
    user = env["res.users"].with_context(active_test=False).search(
        [("login", "=", EDITOR_LOGIN)], limit=1,
    )
    if user:
        if not user.active:
            user.active = True
        user.write({"name": EDITOR_NAME, "email": EDITOR_EMAIL})
        if user.partner_id:
            user.partner_id.write({"name": EDITOR_NAME, "email": EDITOR_EMAIL})
        # Ensure internal user group membership.
        group_user = env.ref("base.group_user")
        if group_user.id not in user.group_ids.ids:
            user.write({"group_ids": [(4, group_user.id)]})
        return user

    group_user = env.ref("base.group_user")
    return env["res.users"].create({
        "login": EDITOR_LOGIN,
        "name": EDITOR_NAME,
        "email": EDITOR_EMAIL,
        "password": EDITOR_LOGIN,
        "group_ids": [(6, 0, [group_user.id])],
    })


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

    # --- Editor user (keeps prior partner across runs to avoid orphans) ---
    _ensure_editor(env)

    # --- Post: published, admin author, short content ---
    admin = env.ref("base.user_admin")
    post = env["blog.post"].create({
        "name": POST_NAME,
        "blog_id": blog.id,
        "author_id": admin.partner_id.id,
        "content": POST_CONTENT,
        "is_published": True,
        "website_published": True,
    })
    # Guarantee the published flags are on (create() may not honor both
    # when website_published is computed in older variants).
    if not post.is_published or not post.website_published:
        post.write({"is_published": True, "website_published": True})
