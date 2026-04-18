"""Cleanup for project_todo.create_note_set_color_deadline."""


def cleanup(env):
    env["project.task"].with_context(active_test=False).search([
        ("name", "=", "Crane Audit Memo"),
    ]).unlink()
