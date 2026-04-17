"""Clean up artifacts from previous runs."""


PROJECT_NAME = "Benchmark Drag Project"
ALPHA_NAME = "Benchmark Card Alpha"
BETA_NAME = "Benchmark Card Beta"


def cleanup(env):
    tasks = env["project.task"].with_context(active_test=False).search([
        ("name", "in", [ALPHA_NAME, BETA_NAME]),
    ])
    tasks.unlink()

    project = env["project.project"].search(
        [("name", "=", PROJECT_NAME)], limit=1
    )
    if project:
        env["project.task"].with_context(active_test=False).search([
            ("project_id", "=", project.id),
        ]).unlink()
        project.unlink()
