"""Seed for website.create_blog_post_publish.

Removes any prior post titled 'Product Launch Announcement' so the agent
starts from a clean state. Ensures the default 'Our blog' exists so the
agent has somewhere to publish the post.
"""


def setup(env):
    # Clean up any prior runs.
    env["blog.post"].with_context(active_test=False).search([
        ("name", "=", "Product Launch Announcement"),
    ]).unlink()

    # Ensure the default blog exists (demo data ships with 'Our blog'; if a
    # prior cleanup deleted it, recreate it so the task is doable).
    if not env["blog.blog"].with_context(active_test=False).search([
        ("name", "=", "Our blog"),
    ], limit=1):
        env["blog.blog"].create({"name": "Our blog"})
