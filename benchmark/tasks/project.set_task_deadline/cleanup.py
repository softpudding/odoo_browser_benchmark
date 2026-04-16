"""Clean up artifacts from previous runs."""


def cleanup(env):
    env["project.task"].search([("name", "=", "Design Landing Page Mockup")]).unlink()