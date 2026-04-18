# project.create_milestone_assign_tasks_reach — Odoo 19 cookbook

## `project.milestone` gating + embedded action entry point

- `project.milestone` is gated per-project by `project.project.allow_milestones`
  (Boolean, default False on fresh `create()`). Seeds must explicitly set
  `allow_milestones=True` or the Milestones tab is hidden from the project
  dashboard and the per-task `milestone_id` field is `invisible="not
  allow_milestones"` on the main form group.
- Visibility of the Milestones action also requires the
  `project.group_project_milestone` ACL. In Odoo 19 this group is implied by
  `base.group_user` through `addons/project/data/project_demo.xml`, so admin
  inherits it in a clean base snapshot. Seed still idempotently ensures the
  admin is in the group to survive future base-snapshot churn.
- Entry point is an `ir.embedded.actions` row
  (`project.project_embedded_action_project_milestones`) registered under
  the "Tasks" action on `project.project`. It shows up as the
  **"Milestones"** breadcrumb / top-menu button inside the project's task
  view — NOT as a tab in the project form. Browser-use consistently
  struggles to discover this: it spent 27 steps hunting the panel before
  clicking the right Top Menu entry in the calibration run.

## `project.milestone.is_reached` — null vs true in state-diff

- `is_reached` is a Boolean with `default=False`. On a record created and
  then `is_reached=True` in the same task, the state-diff engine emits
  `op: "create"` with `norm_value: true` (NOT a separate `set`).
- If the agent creates the milestone but never flips the Boolean, the diff
  row materialises as `op: "create"` with `norm_value: null` (same
  null-vs-false pattern as the `website_blog` archive note in
  `ODOO19_PATTERNS.md`). `expected_state.json` must encode `true` for the
  success row; the partial-BU failure emits `null` and therefore scores as
  an "extra" diff row, not a "missing" one.

## `project.milestone.toggle_is_reached(is_reached)` — agent-visible method

- `project.milestone` exposes `toggle_is_reached(is_reached)` which calls
  `self.update({'is_reached': is_reached})` and returns the record's public
  data dict (see `addons/project/models/project_milestone.py:101`). The
  kanban view widget `task_done_checkmark` binds to this; backend list
  view clicks `is_reached` cell directly via `write`. Either trace op is
  fine — oracle uses `write`, BU uses `web_save`; leave both in
  `optional_ops`.

## `project.task.milestone_id` domain and compute

- `project.task.milestone_id` is a `compute='_compute_milestone_id',
  store=True, readonly=False` many2one with
  `domain="[('project_id', '=', project_id)]"`. That means:
  1. Autocomplete on the task form is scoped to the current project's
     milestones only — no distractor-project milestones appear.
  2. Writing `project_id` on a task with a milestone pinned to the old
     project silently nulls `milestone_id` via the guard in
     `project.task.write` (see `project_task.py::1219-1233`). Tasks in
     this benchmark never re-parent project, so the guard is inert, but
     keep it in mind when reusing this pattern.

## State-diff match_key for `project.milestone`

- Use `match_key: [project_id, name]` so the diff keys as
  `["Bench Milestone Proj", "Phase 1 Complete"]`. Keying on `name` alone
  risks collision with any other project's milestone, and keying on
  `project_id` alone can't distinguish two milestones on the same project
  (future tasks that create multiple milestones would need name as well).
- `reached_date` is a computed-stored Date depending on `is_reached`. It
  appears in post-state captures once is_reached flips True — add it to
  `ignore_fields` to avoid timezone-sensitive diff noise (the BU run can
  cross a midnight boundary if the agent stalls long enough).

## Inline list-edit save timing (browser-use pitfall)

- The Milestones list view is `editable="bottom"` with a `handle` sequence
  column. Clicking "New", typing the name, tabbing into Deadline, typing
  the date, and then pressing "Save" on the form-level save button
  persists — but BU frequently clicks "New" again instead of a list save
  button, spawning a second draft row. Pattern observed in calibration
  stdout at Step 47-48: BU clicks "New" after typing the milestone name,
  losing the first row. Guard in `check.py` with an exact-one assertion on
  `project.milestone` count for this project.

## Distractor T3 ignored naturally

- Browser-use never tried to assign `milestone_id` to T3 in the
  calibration run. The prompt's explicit "Do NOT assign T3" rule
  combined with BU's inability to finish T1/T2 means the distractor trap
  is latent: it isn't what failed BU, but it would catch a smarter agent
  that blindly applies the action to the full list. Keep the asymmetry.
