"""Postcondition checks for project_todo.create_note_add_tag_checklist.

Validates:
1. Exactly one project.task named 'Bench Todo Note' exists and is active.
2. The note carries the 'BenchTag' tag.
3. The note's description contains a checklist item with text 'First step'.
"""

import re


TARGET_NAME = "Bench Todo Note"
TARGET_TAG = "BenchTag"
CHECKLIST_ITEM = "First step"


def _strip_tags(html):
    if not html:
        return ""
    # Remove HTML tags but keep text content
    return re.sub(r"<[^>]+>", " ", html)


def check(env):
    failures = []

    tasks = env["project.task"].with_context(active_test=False).search([
        ("name", "=", TARGET_NAME),
    ])
    if not tasks:
        return [f"Note {TARGET_NAME!r} not found"]
    if len(tasks) != 1:
        return [f"Expected exactly one note named {TARGET_NAME!r}, found {len(tasks)}"]

    task = tasks[0]

    if not task.active:
        failures.append("Note should remain active")

    tag_names = set(task.tag_ids.mapped("name"))
    if TARGET_TAG not in tag_names:
        failures.append(
            f"Note is missing the {TARGET_TAG!r} tag (has {sorted(tag_names)})"
        )

    description = task.description or ""
    # Require a checklist block and the expected text.
    has_checklist_structure = (
        "o_checklist" in description
        or 'data-list="checklist"' in description
        or "data-checked" in description
    )
    if not has_checklist_structure:
        failures.append(
            "Description does not contain a checklist block "
            "(expected <ul class=\"o_checklist\"> or data-list=\"checklist\")"
        )

    stripped = _strip_tags(description)
    normalized = " ".join(stripped.split())
    if CHECKLIST_ITEM.lower() not in normalized.lower():
        failures.append(
            f"Description does not contain checklist text {CHECKLIST_ITEM!r}"
        )

    return failures
