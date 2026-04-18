"""Seed for website_blog.create_tag_assign_to_three_posts.

Category: deep_ui_interaction (MEDIUM).

Bulk tag assignment: the agent must create one blog.tag ('Q2-2026')
and then open three seeded posts (Post-A, Post-B, Post-C) one by one to
add the new tag on each post's tag_ids m2m. A distractor post Post-D
must NOT receive the tag (punishes the "select all posts" shortcut
through the tag form's reverse post_ids m2m).

Starting state:
- No 'Q2-2026' tag exists.
- One blog 'Harbor Quarterly' exists (created here) containing four
  unpublished blog.post records: Post-A, Post-B, Post-C, Post-D.
- None of the posts carry any tags initially.
"""


BLOG_NAME = "Harbor Quarterly"
TAG_NAME = "Q2-2026"
POST_NAMES = ["Post-A", "Post-B", "Post-C", "Post-D"]


def setup(env):
    # --- Cleanup prior runs ---
    env["blog.post"].with_context(active_test=False).search(
        [("name", "in", POST_NAMES)],
    ).unlink()
    env["blog.tag"].search([("name", "=", TAG_NAME)]).unlink()
    env["blog.blog"].with_context(active_test=False).search(
        [("name", "=", BLOG_NAME)],
    ).unlink()

    # --- Blog ---
    blog = env["blog.blog"].create({"name": BLOG_NAME})

    # --- Posts: all unpublished, no tags, short deterministic subtitle ---
    for name in POST_NAMES:
        env["blog.post"].create({
            "name": name,
            "blog_id": blog.id,
            "subtitle": f"Seed post {name}",
            "content": f"<p>Body of {name}.</p>",
            "tag_ids": [(6, 0, [])],
            "is_published": False,
            "website_published": False,
        })
