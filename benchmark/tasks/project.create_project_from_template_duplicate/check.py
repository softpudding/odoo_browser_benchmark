"""Postcondition checks for project.create_project_from_template_duplicate.

Validates:
1. Original 'Bench Template Project' still exists and still has its 3 tasks.
2. Exactly one 'Bench Template Project (Copy)' exists.
3. The copy has exactly 3 tasks named {Setup, Build, Review}.
"""


PROJECT_NAME = "Bench Template Project"
COPY_NAME = "Bench Template Project (Copy)"
TASK_NAMES = {"Setup", "Build", "Review"}


def check(env):
    failures = []

    # --- Original project preserved ---
    originals = env["project.project"].search([("name", "=", PROJECT_NAME)])
    if len(originals) == 0:
        return [f"Original project '{PROJECT_NAME}' is missing"]
    if len(originals) > 1:
        failures.append(
            f"Expected exactly 1 '{PROJECT_NAME}', found {len(originals)}"
        )
    original = originals[:1]

    original_tasks = env["project.task"].with_context(active_test=False).search([
        ("project_id", "=", original.id),
    ])
    original_task_names = {t.name for t in original_tasks}
    if original_task_names != TASK_NAMES:
        failures.append(
            f"Original project tasks changed: got {sorted(original_task_names)}, "
            f"expected {sorted(TASK_NAMES)}"
        )

    # --- Copy exists exactly once ---
    copies = env["project.project"].search([("name", "=", COPY_NAME)])
    if len(copies) == 0:
        failures.append(f"Copy project '{COPY_NAME}' is missing")
        return failures
    if len(copies) > 1:
        failures.append(
            f"Expected exactly 1 '{COPY_NAME}', found {len(copies)}"
        )
    copy = copies[:1]

    if copy.id == original.id:
        failures.append("Copy and original resolve to the same project record")
        return failures

    # --- Copy has the right tasks ---
    copy_tasks = env["project.task"].with_context(active_test=False).search([
        ("project_id", "=", copy.id),
    ])
    copy_task_names = {t.name for t in copy_tasks}
    if copy_task_names != TASK_NAMES:
        failures.append(
            f"Copy project tasks are {sorted(copy_task_names)}, "
            f"expected {sorted(TASK_NAMES)}"
        )
    if len(copy_tasks) != 3:
        failures.append(
            f"Copy project has {len(copy_tasks)} tasks, expected exactly 3"
        )

    return failures
