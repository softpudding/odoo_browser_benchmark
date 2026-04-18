"""Seed for project_todo.create_note_set_color_deadline."""


TARGET_NAME = "Crane Audit Memo"


def setup(env):
    env["project.task"].with_context(active_test=False).search([
        ("name", "=", TARGET_NAME),
    ]).unlink()
