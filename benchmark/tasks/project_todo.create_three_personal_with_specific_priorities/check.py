"""Postcondition checks for project_todo.create_three_personal_with_specific_priorities.

Validates:
1. Each of the three named todos exists and is active.
2. 'Plan Sprint' has priority='1' (single star / High).
3. 'Write Docs' and 'Refactor CSS' keep the default priority='0'.
4. None of the todos got extra tags or deadlines (basic anti-modification check).
"""


EXPECTED_PRIORITY = {
    "Plan Sprint": "1",
    "Write Docs": "0",
    "Refactor CSS": "0",
}


def check(env):
    failures = []

    for name, expected_priority in EXPECTED_PRIORITY.items():
        tasks = env["project.task"].with_context(active_test=False).search([
            ("name", "=", name),
        ])
        if not tasks:
            failures.append(f"To-do '{name}' not found")
            continue
        if len(tasks) > 1:
            failures.append(
                f"Expected exactly one to-do named '{name}', found {len(tasks)}"
            )
            continue

        task = tasks
        if not task.active:
            failures.append(f"To-do '{name}' should remain active but was archived")

        actual_priority = task.priority or "0"
        if actual_priority != expected_priority:
            failures.append(
                f"To-do '{name}' priority is {actual_priority!r}, "
                f"expected {expected_priority!r}"
            )

        if task.tag_ids:
            tag_names = sorted(task.tag_ids.mapped("name"))
            failures.append(
                f"To-do '{name}' should not have tags but has {tag_names}"
            )

        if task.date_deadline:
            failures.append(
                f"To-do '{name}' should not have a deadline but has {task.date_deadline}"
            )

    return failures
