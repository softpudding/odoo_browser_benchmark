"""Clean up website.create_blog_post_publish artifacts."""


def cleanup(env):
    module = env["ir.module.module"].search([
        ("name", "=", "website_blog"),
        ("state", "=", "installed"),
    ], limit=1)
    if module:
        env["blog.post"].search([("name", "=", "Warehouse Automation Trends 2026")]).unlink()

