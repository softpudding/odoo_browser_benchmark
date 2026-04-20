"""Check website_blog.duplicate_post_localize_seo_slug_publish."""

def check(env):
    failures = []
    source = env["blog.post"].with_context(active_test=False).search([("name", "=", "Warehouse Safety Primer")], limit=1)
    dup = env["blog.post"].with_context(active_test=False).search([("name", "=", "Warehouse Safety Primer EU")], limit=1)
    if not source:
        return ["Source post missing"]
    if not dup:
        return ["Duplicate post missing"]
    if source.website_published or source.is_published:
        failures.append("Source post should remain unpublished")
    if not dup.website_published:
        failures.append("Duplicate post is not published")
    if dup.website_meta_title != "Warehouse Safety Primer for EU Teams":
        failures.append(f"SEO title is {dup.website_meta_title!r}")
    if dup.website_meta_description != "Safety baseline for EU warehouse operations and dock checks.":
        failures.append(f"SEO description is {dup.website_meta_description!r}")
    return failures
