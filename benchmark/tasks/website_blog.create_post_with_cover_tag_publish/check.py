"""Postcondition checks for website_blog.create_post_with_cover_tag_publish."""


def check(env):
    failures = []

    post = env["blog.post"].with_context(active_test=False).search([
        ("name", "=", "Harbor Notes Rollout"),
    ], limit=1)
    if not post:
        return ["Blog post 'Harbor Notes Rollout' not found"]

    if not post.blog_id or post.blog_id.name != "Harbor Newsroom":
        failures.append(f"Blog is {post.blog_id.name!r}")
    if not post.website_published:
        failures.append("Blog post is not published")
    if post.subtitle != "Dock updates for the late-summer operations release.":
        failures.append(f"Subtitle is {post.subtitle!r}")
    if "Operations Spotlight" not in post.tag_ids.mapped("name"):
        failures.append(f"Tags are {post.tag_ids.mapped('name')!r}")
    if "background-image" not in (post.cover_properties or ""):
        failures.append("Cover image metadata is missing")

    return failures
