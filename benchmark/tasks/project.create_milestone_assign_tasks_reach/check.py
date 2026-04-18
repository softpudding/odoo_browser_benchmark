"""Postcondition checks for project.create_milestone_assign_tasks_reach.

Validates:
1. Project 'Bench Milestone Proj' still exists with allow_milestones=True.
2. Exactly one milestone 'Phase 1 Complete' with deadline 2026-06-01 and
   is_reached=True.
3. Task T1 + T2 both have milestone_id = 'Phase 1 Complete'.
4. Task T3 still has no milestone set (distractor).
5. No new tasks created; project still has exactly 3 tasks.
6. No task renamed or archived.
"""

from datetime import date


PROJECT_NAME = "Bench Milestone Proj"
MILESTONE_NAME = "Phase 1 Complete"
EXPECTED_DEADLINE = date(2026, 6, 1)

TASK_T1 = "T1 - Draft Spec"
TASK_T2 = "T2 - Build Prototype"
TASK_T3 = "T3 - Review Final"

ASSIGNED_TASKS = [TASK_T1, TASK_T2]
ALL_TASK_NAMES = [TASK_T1, TASK_T2, TASK_T3]


def check(env):
    failures = []

    project = env["project.project"].with_context(active_test=False).search([
        ("name", "=", PROJECT_NAME),
    ], limit=1)
    if not project:
        return [f"Project '{PROJECT_NAME}' is missing"]
    if not project.active:
        failures.append(f"Project '{PROJECT_NAME}' was archived")
    if not project.allow_milestones:
        failures.append(
            f"Project '{PROJECT_NAME}' allow_milestones is False — "
            "task required the feature to remain enabled"
        )

    # --- Milestone checks ---
    milestones = env["project.milestone"].search([
        ("project_id", "=", project.id),
    ])
    if len(milestones) == 0:
        failures.append(
            f"Project '{PROJECT_NAME}' has no milestones; "
            f"expected exactly one named '{MILESTONE_NAME}'"
        )
    elif len(milestones) > 1:
        names = milestones.mapped("name")
        failures.append(
            f"Project '{PROJECT_NAME}' has {len(milestones)} milestones "
            f"{names}; expected exactly one named '{MILESTONE_NAME}'"
        )
    else:
        m = milestones[0]
        if m.name != MILESTONE_NAME:
            failures.append(
                f"Milestone name is '{m.name}', expected '{MILESTONE_NAME}'"
            )
        if m.deadline != EXPECTED_DEADLINE:
            failures.append(
                f"Milestone '{MILESTONE_NAME}' deadline is "
                f"{m.deadline}, expected {EXPECTED_DEADLINE}"
            )
        if not m.is_reached:
            failures.append(
                f"Milestone '{MILESTONE_NAME}' is_reached is False; "
                "task required toggling Reached to True"
            )

    # --- Task checks ---
    tasks = env["project.task"].with_context(active_test=False).search([
        ("project_id", "=", project.id),
    ])
    task_by_name = {t.name: t for t in tasks}

    if len(tasks) != 3:
        failures.append(
            f"Project has {len(tasks)} tasks; expected exactly 3"
        )

    for name in ALL_TASK_NAMES:
        t = task_by_name.get(name)
        if not t:
            failures.append(f"Task '{name}' is missing from the project")
            continue
        if not t.active:
            failures.append(f"Task '{name}' is archived")

    # T1 and T2 must be linked to the milestone.
    for name in ASSIGNED_TASKS:
        t = task_by_name.get(name)
        if not t:
            continue
        if not t.milestone_id:
            failures.append(
                f"Task '{name}' has no milestone; expected "
                f"'{MILESTONE_NAME}'"
            )
        elif t.milestone_id.name != MILESTONE_NAME:
            failures.append(
                f"Task '{name}' is linked to milestone "
                f"'{t.milestone_id.name}', expected '{MILESTONE_NAME}'"
            )

    # T3 must NOT be linked to any milestone.
    t3 = task_by_name.get(TASK_T3)
    if t3 and t3.milestone_id:
        failures.append(
            f"Task '{TASK_T3}' is linked to milestone "
            f"'{t3.milestone_id.name}'; prompt forbids assigning a "
            "milestone to this distractor"
        )

    return failures
