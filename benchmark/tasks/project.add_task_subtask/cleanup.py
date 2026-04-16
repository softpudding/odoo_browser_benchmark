"""Clean up artifacts from previous runs."""

SUBTASK_NAME = "Create Wireframes"
TASK_NAME = "Design Landing Page Mockup"


def cleanup(env):
    env["project.task"].search([("name", "=", SUBTASK_NAME)]).unlink()
    env["project.task"].search([("name", "=", TASK_NAME)]).unlink()