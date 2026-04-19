"""Postcondition checks for project.set_task_priority_urgent_assign_tag.

Validates:
1. The 'Fix critical bug' project.task still exists (exactly one, active) on
   the 'Bench Prio Project' project.
2. priority == '1' (Important/High) — was seeded as '0'.
3. tag_ids contains the existing 'Bug' tag (by name, case-insensitive).
4. No duplicate 'Bug' tag was quick-created.
5. Only one task exists on the project (no extras created/deleted).
6. Task name is unchanged.
"""


PROJECT_NAME = "Bench Prio Project"
TASK_NAME = "Fix critical bug"
REQUIRED_TAG_NAME = "Bug"


def check(env):
    failures = []

    project = env["project.project"].search(
        [("name", "=", PROJECT_NAME)], limit=1
    )
    if not project:
        return [f"Project '{PROJECT_NAME}' not found"]

    # 1. Target task exists (exactly one, active).
    tasks = env["project.task"].with_context(active_test=False).search([
        ("name", "=", TASK_NAME),
        ("project_id", "=", project.id),
    ])
    if not tasks:
        failures.append(
            f"Task '{TASK_NAME}' was not found on project '{PROJECT_NAME}'"
        )
        return failures
    if len(tasks) > 1:
        failures.append(
            f"Expected exactly 1 task '{TASK_NAME}', found {len(tasks)}"
        )

    task = tasks[0]
    if not task.active:
        failures.append(f"Task '{TASK_NAME}' is archived (active=False)")

    # 2. priority must be '1' (was '0' in seed). Priority is a Selection
    # ('0'..'3') rendered as a 3-star widget; '1' = exactly one filled star.
    if task.priority != "1":
        failures.append(
            f"Task '{TASK_NAME}' priority is '{task.priority}', expected '1' "
            "(exactly one filled star — do not click more than one star)"
        )

    # 3. tag_ids must contain the required tag (case-insensitive name match).
    actual_tag_names = {t.name.lower() for t in task.tag_ids}
    if REQUIRED_TAG_NAME.lower() not in actual_tag_names:
        failures.append(
            f"Task '{TASK_NAME}' tag_ids missing required tag "
            f"'{REQUIRED_TAG_NAME}' (has {sorted(actual_tag_names)})"
        )

    # 4. No duplicate 'Bug' tag created — exactly one should exist.
    bug_tags = env["project.tags"].with_context(active_test=False).search([
        ("name", "=ilike", REQUIRED_TAG_NAME),
    ])
    if len(bug_tags) == 0:
        failures.append(
            f"Tag '{REQUIRED_TAG_NAME}' no longer exists "
            "(prompt forbids deleting/renaming tags)"
        )
    elif len(bug_tags) > 1:
        failures.append(
            f"Found {len(bug_tags)} tags named '{REQUIRED_TAG_NAME}'; "
            "prompt forbids creating duplicate tags"
        )

    # 5. Exactly one task on the project.
    project_task_count = env["project.task"].search_count([
        ("project_id", "=", project.id),
    ])
    if project_task_count != 1:
        failures.append(
            f"Project '{PROJECT_NAME}' has {project_task_count} tasks, expected 1"
        )

    return failures
