"""Postcondition checks for website.create_blog_post_publish."""


def check(env):
    module = env["ir.module.module"].search([
        ("name", "=", "website_blog"),
        ("state", "=", "installed"),
    ], limit=1)
    if not module:
        return ["website_blog is not installed in benchmark_base"]

    posts = env["blog.post"].search([("name", "=", "Warehouse Automation Trends 2026")])
    if len(posts) != 1:
        return [f"Expected exactly one target blog post, found {len(posts)}"]

    post = posts[0]
    failures = []
    if not post.is_published:
        failures.append("Blog post is not published")
    if post.subtitle != "What operations teams should automate first":
        failures.append(f"Unexpected subtitle: {post.subtitle!r}")
    body = post.content or post.content_html or ""
    if "Warehouse leaders are prioritizing slotting accuracy" not in body:
        failures.append("Expected body text not found in the blog post content")
    if not (post.cover_properties or post.cover_image or post.teaser_image):
        failures.append("No cover image appears to be configured on the blog post")
    return failures
