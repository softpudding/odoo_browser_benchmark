"""Clean up artifacts from previous runs."""


def cleanup(env):
    tasks = env["project.task"].search([
        ("name", "=", "Design Landing Page Mockup"),
    ])
    tasks.unlink()
