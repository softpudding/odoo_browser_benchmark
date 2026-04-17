"""Postcondition checks for project_todo.duplicate_note_retag_archive_original."""


TARGET_NAME = "Welcome Administrator!"
DISTRACTOR_NAME = "Welcome Administrator West"
FOLLOW_UP_NAME = "Welcome Administrator Follow-up"


def check(env):
    failures = []

    original = env["project.task"].with_context(active_test=False).search([
        ("name", "=", TARGET_NAME),
    ], limit=1)
    if not original:
        return [f"Original note '{TARGET_NAME}' not found"]

    if original.active:
        failures.append("Original note should be archived")
    if "Needs Review" not in original.tag_ids.mapped("name"):
        failures.append("Original note lost the 'Needs Review' tag")

    follow_up = env["project.task"].with_context(active_test=False).search([
        ("name", "=", FOLLOW_UP_NAME),
    ], limit=1)
    if not follow_up:
        failures.append(f"Duplicate note '{FOLLOW_UP_NAME}' not found")
    else:
        if not follow_up.active:
            failures.append("Duplicate note should remain active")
        tag_names = set(follow_up.tag_ids.mapped("name"))
        if tag_names != {"Harbor Ops"}:
            failures.append(
                f"Duplicate note tags are {sorted(tag_names)}, expected only ['Harbor Ops']"
            )

    distractor = env["project.task"].with_context(active_test=False).search([
        ("name", "=", DISTRACTOR_NAME),
    ], limit=1)
    if not distractor:
        failures.append(f"Distractor note '{DISTRACTOR_NAME}' not found")
    elif not distractor.active:
        failures.append("Distractor note should stay active")

    return failures
