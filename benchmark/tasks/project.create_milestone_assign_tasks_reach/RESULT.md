# project.create_milestone_assign_tasks_reach — eval record

## Status summary

| Dimension | Result |
|---|---|
| **Oracle** | PASS |
| **Browser-Use** | FAIL (single-shot) |
| **StateDiffF1** | 0.0 |
| **Oracle wall clock** | 18.7 s |
| **Browser-Use wall clock** | 360.0 s (hit time_limit_sec) |

## Oracle run

- Mode: JSON-RPC `call_kw` sequence — `project.milestone.create`,
  `project.task.web_save { milestone_id: ... }` x2, `project.milestone.write
  { is_reached: true }`.
- 6 expected atomic edits, 6 observed, 0 missing, 0 extra → F1 = 1.0.
- No forbidden ops recorded. Trace clean.

## Browser-Use run (auto-isolated, bu-1-0, 360 s cap)

- Agent created the milestone `Phase 1 Complete` with deadline
  `2026-06-01` successfully via the embedded Milestones top-menu (after
  ~27 wasted steps hunting for the right entry point).
- Then spent the remainder of the budget bouncing between the Tasks list
  and T1's form without ever successfully committing `milestone_id` on
  T1 or T2 (autocomplete + Save chain kept reverting).
- Never flipped `is_reached` on the milestone.
- Final state diff: 4 observed (milestone create) vs 6 expected
  (milestone create + 2 task-milestone assigns + 1 is_reached write).
  Precision / Recall = 0 / 0 by the binariser (Recall=3/6=0.5).
- Postcondition failures recorded:
  - Milestone `Phase 1 Complete` is_reached is False.
  - Task `T1 - Draft Spec` has no milestone.
  - Task `T2 - Build Prototype` has no milestone.
- Extra diff:
  `project.milestone.is_reached = None` (BU-initiated web_save that did
  not commit a True value — shows up as a create-time null slot).

## Calibration verdict

- **Medium tier, tier: 2** — workflow requires discovering the
  project Milestones embedded panel (kebab / Top Menu), creating a
  record via the inline-list editor, returning to the task list,
  per-task milestone many2one autocomplete save x2, then flipping a
  Boolean back on the milestone. Five distinct UI surfaces in one task.
- BU single-shot calibrated FAIL. Even with the seed already enabling
  `allow_milestones`, BU loses ~27 steps on panel discovery and can
  only complete 1 of the 4 required writes.
- Distractor T3 remained untouched in the BU run (no false-positive
  assignment) — the three-task distractor design is effective at
  catching "assign all tasks" fallback behaviour without making the
  task ambiguous.

## Failure patterns exercised

- Embedded-action "Milestones" tab discovery (project.project →
  `project.milestone_action` via `ir.embedded.actions`).
- Inline-editable list save + Deadline date commit inside
  `project_milestone_view_tree`.
- Per-record `milestone_id` many2one autocomplete on the task form
  (same fragile dropdown pattern as project_id in
  `project_todo.bulk_move_tasks_between_projects`).
- Boolean toggle (`is_reached`) re-open on a record the agent
  already finished editing — classic "return and tick" miss.
