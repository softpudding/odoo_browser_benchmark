"""Cleanup for project.create_subtask_assign_deadline."""


def cleanup(env):
    env["project.project"].search([("name", "=", "Atlas Implementation Sprint")]).unlink()
