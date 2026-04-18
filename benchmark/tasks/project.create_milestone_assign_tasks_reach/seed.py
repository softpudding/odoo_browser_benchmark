"""Seed for project.create_milestone_assign_tasks_reach.

MEDIUM (tier 2). Test: open an existing project that already has
milestones enabled, create a fresh `project.milestone` named 'Phase 1
Complete' with deadline 2026-06-01 via the project's **Milestones** tab,
then assign two tasks (T1 + T2) to the new milestone via the per-task
form edit, and finally mark the milestone as reached (`is_reached=True`).

A third distractor task T3 must remain unassigned to any milestone.

Seeded state:
  - project.project 'Bench Milestone Proj' with allow_milestones=True
  - No pre-existing milestones on the project (so creation is required)
  - Three tasks, all currently with `milestone_id = False`:
      - "T1 - Draft Spec"
      - "T2 - Build Prototype"
      - "T3 - Review Final"  (distractor)
"""

PROJECT_NAME = "Bench Milestone Proj"
MILESTONE_NAME = "Phase 1 Complete"

TASK_T1 = "T1 - Draft Spec"
TASK_T2 = "T2 - Build Prototype"
TASK_T3 = "T3 - Review Final"

ALL_TASK_NAMES = [TASK_T1, TASK_T2, TASK_T3]


def setup(env):
    # --- Cleanup prior runs (child-first ordering) ---
    env["project.task"].with_context(active_test=False).search([
        ("name", "in", ALL_TASK_NAMES),
    ]).unlink()

    old_project = env["project.project"].with_context(active_test=False).search([
        ("name", "=", PROJECT_NAME),
    ])
    for p in old_project:
        env["project.milestone"].search([("project_id", "=", p.id)]).unlink()
        env["project.task"].with_context(active_test=False).search([
            ("project_id", "=", p.id),
        ]).unlink()
    old_project.unlink()

    # --- Ensure admin carries the Use Milestones group (normally implied
    #     via group_user → group_project_milestone but we confirm). ---
    admin = env.ref("base.user_admin")
    milestone_grp = env.ref("project.group_project_milestone")
    if admin.id not in milestone_grp.user_ids.ids:
        milestone_grp.user_ids = [(4, admin.id)]

    # --- Create the project with milestones already enabled. ---
    project = env["project.project"].create({
        "name": PROJECT_NAME,
        "allow_milestones": True,
    })

    # --- Create the three tasks, all without a milestone. ---
    for name in ALL_TASK_NAMES:
        env["project.task"].create({
            "name": name,
            "project_id": project.id,
        })

    # Sanity checks so the oracle/human runner has a predictable start state.
    tasks = env["project.task"].search([("project_id", "=", project.id)])
    assert len(tasks) == 3, (
        f"seed: expected 3 tasks under {PROJECT_NAME}, got {len(tasks)}"
    )
    assert all(not t.milestone_id for t in tasks), (
        "seed: all seeded tasks must start without a milestone"
    )
    existing = env["project.milestone"].search([("project_id", "=", project.id)])
    assert len(existing) == 0, (
        f"seed: {PROJECT_NAME} must start with no milestones, got {len(existing)}"
    )
    assert project.allow_milestones, (
        "seed: allow_milestones must be True on the project"
    )
