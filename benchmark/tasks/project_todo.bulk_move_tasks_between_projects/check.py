"""Postcondition checks for project_todo.bulk_move_tasks_between_projects.

Validates:
1. Bench Task Alpha, Bravo, Charlie all have project_id = Bench Proj B.
2. Bench Task Delta stays in Bench Proj A (distractor must NOT be moved).
3. Bench Proj A contains exactly 1 active task.
4. Bench Proj B contains exactly 3 active tasks.
5. No extra project.task records were created under the canonical names.
6. No task was archived (active=True) or renamed.
"""


PROJECT_A = "Bench Proj A"
PROJECT_B = "Bench Proj B"

TASK_ALPHA = "Bench Task Alpha"
TASK_BRAVO = "Bench Task Bravo"
TASK_CHARLIE = "Bench Task Charlie"
TASK_DELTA = "Bench Task Delta"

TO_MOVE = [TASK_ALPHA, TASK_BRAVO, TASK_CHARLIE]
ALL_TASK_NAMES = TO_MOVE + [TASK_DELTA]


def _find_task(env, name):
    return env["project.task"].with_context(active_test=False).search([
        ("name", "=", name),
    ])


def check(env):
    failures = []

    proj_a = env["project.project"].search([("name", "=", PROJECT_A)], limit=1)
    proj_b = env["project.project"].search([("name", "=", PROJECT_B)], limit=1)

    if not proj_a:
        failures.append(f"Project '{PROJECT_A}' is missing")
    if not proj_b:
        failures.append(f"Project '{PROJECT_B}' is missing")
    if failures:
        return failures

    # 1. Each of the three target tasks must now live in Bench Proj B.
    for name in TO_MOVE:
        tasks = _find_task(env, name)
        if not tasks:
            failures.append(f"Task '{name}' is missing")
            continue
        if len(tasks) > 1:
            failures.append(
                f"Task '{name}': found {len(tasks)} records, expected 1"
            )
            continue
        t = tasks[0]
        if not t.active:
            failures.append(f"Task '{name}' is archived (active=False)")
        if t.project_id.id != proj_b.id:
            failures.append(
                f"Task '{name}' is in project "
                f"'{t.project_id.name}', expected '{PROJECT_B}'"
            )

    # 2. Delta must remain in Bench Proj A.
    delta = _find_task(env, TASK_DELTA)
    if not delta:
        failures.append(f"Task '{TASK_DELTA}' is missing (must remain in A)")
    elif len(delta) > 1:
        failures.append(
            f"Task '{TASK_DELTA}': {len(delta)} records, expected exactly 1"
        )
    else:
        d = delta[0]
        if not d.active:
            failures.append(f"Task '{TASK_DELTA}' is archived")
        if d.project_id.id != proj_a.id:
            failures.append(
                f"Task '{TASK_DELTA}' is in project "
                f"'{d.project_id.name}', expected '{PROJECT_A}' "
                f"(task explicitly forbids moving this distractor)"
            )

    # 3/4. Per-project task counts.
    a_active = env["project.task"].search_count([
        ("project_id", "=", proj_a.id),
        ("active", "=", True),
    ])
    if a_active != 1:
        failures.append(
            f"'{PROJECT_A}' has {a_active} active tasks, expected 1 (Delta)"
        )

    b_active = env["project.task"].search_count([
        ("project_id", "=", proj_b.id),
        ("active", "=", True),
    ])
    if b_active != 3:
        failures.append(
            f"'{PROJECT_B}' has {b_active} active tasks, "
            f"expected 3 (Alpha, Bravo, Charlie)"
        )

    # 5. No extra canonical-named records — each of our four names maps to exactly one task.
    all_named = env["project.task"].with_context(active_test=False).search([
        ("name", "in", ALL_TASK_NAMES),
    ])
    if len(all_named) != len(ALL_TASK_NAMES):
        failures.append(
            f"Expected {len(ALL_TASK_NAMES)} canonical named tasks, "
            f"found {len(all_named)}"
        )

    return failures
