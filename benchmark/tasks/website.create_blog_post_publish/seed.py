"""Seed website.create_blog_post_publish.

Requires the optional website_blog module. The base snapshot currently does not
include it, so this task is scaffolded but not runnable until that module is
added to the benchmark base.
"""


def setup(env):
    module = env["ir.module.module"].search([
        ("name", "=", "website_blog"),
        ("state", "=", "installed"),
    ], limit=1)
    if not module:
        raise ValueError(
            "website_blog is not installed in benchmark_base; install it before running website.create_blog_post_publish"
        )

    blog = env["blog.blog"].search([("name", "=", "Operations Insights")], limit=1)
    if not blog:
        blog = env["blog.blog"].create({"name": "Operations Insights", "website_id": 1})

    env["blog.post"].search([("name", "=", "Warehouse Automation Trends 2026")]).unlink()
    env.cr.commit()
