"""Seed for project_todo.create_note_add_tag_checklist.

Ensures the 'Bench Sprint' tag exists and removes any leftover note
named 'Sprint planning notes' from prior runs.
"""


TARGET_NAME = "Sprint planning notes"
TARGET_TAG = "Bench Sprint"


def setup(env):
    # Clean up any prior note with the target name so the task always
    # starts from a state where it has not been created yet.
    env["project.task"].with_context(active_test=False).search([
        ("name", "=", TARGET_NAME),
    ]).unlink()

    # Ensure the Bench Sprint tag exists (the prompt says "existing tag").
    tag = env["project.tags"].search([("name", "=", TARGET_TAG)], limit=1)
    if not tag:
        env["project.tags"].create({"name": TARGET_TAG})
