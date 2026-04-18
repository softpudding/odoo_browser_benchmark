"""Postcondition checks for website.create_blog_post_publish."""


def check(env):
    failures = []

    posts = env["blog.post"].with_context(active_test=False).search([
        ("name", "=", "Product Launch Announcement"),
    ])
    if not posts:
        return ["Blog post 'Product Launch Announcement' not found"]
    if len(posts) > 1:
        failures.append(
            f"Expected a single post, found {len(posts)} with this title"
        )

    post = posts[:1]

    if not post.blog_id or post.blog_id.name != "Our blog":
        failures.append(f"Blog is {post.blog_id.name!r}, expected 'Our blog'")

    if post.subtitle != "Announcing our newest product lineup for Q2.":
        failures.append(f"Subtitle is {post.subtitle!r}")

    if not post.is_published:
        failures.append("Blog post is not published (is_published is False)")

    return failures
