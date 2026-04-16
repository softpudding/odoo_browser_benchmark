"""Cleanup for project.set_project_deadline_tags."""

PROJECT_NAME = "Meridian Platform Build"
DISTRACTOR_PROJECT = "Meridian Dev Tools"


def cleanup(env):
    for name in [PROJECT_NAME, DISTRACTOR_PROJECT]:
        projects = env["project.project"].search([("name", "=", name)])
        for project in projects:
            project.task_ids.unlink()
            project.unlink()
