"""Postcondition checks for website_blog.change_author_republish_post.

Validates:
1. Exactly one blog.post named 'Bench Blog Post' exists.
2. Its author_id equals the partner of the seeded 'bench_editor' user.
3. is_published and website_published remain True (must still be published).
4. Title, blog, content unchanged from seed.
"""


POST_NAME = "Bench Blog Post"
BLOG_NAME = "Bench News"
EDITOR_LOGIN = "bench_editor"
EDITOR_NAME = "Bench Editor"


def check(env):
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

    # Author must be Bench Editor's partner
    editor_user = env["res.users"].with_context(active_test=False).search(
        [("login", "=", EDITOR_LOGIN)], limit=1,
    )
    if not editor_user:
        failures.append(f"Seeded user '{EDITOR_LOGIN}' not found")
    else:
        if not post.author_id:
            failures.append("Post has no author; expected Bench Editor")
        elif post.author_id.id != editor_user.partner_id.id:
            failures.append(
                "Post author_id is "
                f"{post.author_id.display_name!r} (id={post.author_id.id}), "
                f"expected {EDITOR_NAME!r} "
                f"(partner id={editor_user.partner_id.id})"
            )

    # Must remain published
    if not post.is_published:
        failures.append(
            f"Post is_published is {post.is_published!r}, expected True"
        )
    if not post.website_published:
        failures.append(
            f"Post website_published is {post.website_published!r}, expected True"
        )

    # Title unchanged
    if post.name != POST_NAME:
        failures.append(f"Post name is {post.name!r}, expected {POST_NAME!r}")

    # Content unchanged (seeded marker phrase present)
    if not post.content or "body of the Bench Blog Post" not in (post.content or ""):
        failures.append(
            "Post content appears modified — seeded marker phrase missing"
        )

    return failures
