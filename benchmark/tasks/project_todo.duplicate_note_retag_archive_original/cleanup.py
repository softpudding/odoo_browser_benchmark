"""Cleanup for project_todo.duplicate_note_retag_archive_original."""


def cleanup(env):
    env["project.task"].with_context(active_test=False).search([
        ("name", "in", [
            "Welcome Administrator West",
            "Welcome Administrator Follow-up",
        ]),
    ]).unlink()
