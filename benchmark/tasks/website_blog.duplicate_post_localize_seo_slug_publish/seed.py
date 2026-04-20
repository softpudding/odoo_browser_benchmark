"""Seed for website_blog.duplicate_post_localize_seo_slug_publish."""

def setup(env):
    env["blog.post"].with_context(active_test=False).search([("name", "in", ["Warehouse Safety Primer", "Warehouse Safety Primer EU"])]).unlink()
    env["blog.blog"].with_context(active_test=False).search([("name", "=", "Bench Ops Blog")]).unlink()
    blog = env["blog.blog"].create({"name": "Bench Ops Blog"})
    env["blog.post"].create({
        "name": "Warehouse Safety Primer",
        "blog_id": blog.id,
        "author_id": env.ref("base.user_admin").partner_id.id,
        "content": "<p>Original warehouse primer content.</p>",
        "is_published": False,
        "website_published": False,
    })
