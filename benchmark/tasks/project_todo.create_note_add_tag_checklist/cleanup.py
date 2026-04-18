"""Cleanup for project_todo.create_note_add_tag_checklist."""


TARGET_NAME = "Bench Todo Note"
TARGET_TAG = "BenchTag"


def cleanup(env):
    env["project.task"].with_context(active_test=False).search([
        ("name", "=", TARGET_NAME),
    ]).unlink()

    env["project.tags"].search([("name", "=", TARGET_TAG)]).unlink()
