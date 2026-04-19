# Cookbook notes — project.create_task_with_deadline_tags_assignees

## `project.task.date_deadline` is a Datetime, not a Date

In Odoo 19 `project.task.date_deadline = fields.Datetime(string='Deadline', ...)`
(`addons/project/models/project_task.py:183`). The form renders it with a
date-only widget, but the ORM stores a UTC datetime shifted by the user's
timezone.

Consequence for check.py: when the agent types `06/30/2026`, the stored value
is `2026-06-30 00:00:00` in the admin's local TZ (America/Los_Angeles in the
benchmark snapshot) which serializes as `2026-06-29 16:00:00 UTC`. A naive
`task.date_deadline == date(2026, 6, 30)` comparison fails. Convert
UTC -> admin-local date before comparing:

```python
import pytz
tz = pytz.timezone(env.user.tz or "UTC")
actual = pytz.UTC.localize(task.date_deadline).astimezone(tz).date()
```

Same trick is used in `project_todo.reorder_notes_add_due_dates_bulk/check.py`.

## New project.task records emit both `name` and `active` create edits

A freshly-created `project.task` produces TWO atomic `op=create` edits:

```json
[
  {"field":"name",   "op":"create", "norm_value":"Fix login bug"},
  {"field":"active", "op":"create", "norm_value":true}
]
```

`active` has default=True on the model and the diff engine emits it alongside
`name`. Include BOTH in `expected_state.json` or F1 drops to 0.67 / 0.0
depending on which direction the asymmetry lands on. Same pattern as
`project.task.type` creates (see `project.create_kanban_stage_reorder_drag`).

## Inline quick-create on project kanban vs full form

Clicking the control-panel **New** on a project's task kanban normally inserts
an inline quick-create row into the **first column** with ONLY a Title input.
To get a full form (Deadline / Tags / Assignees visible), either:

1. **Switch to list view first**, then click **New** → opens the form.
2. OR submit the title row (Enter), then click the row to open the task form.

The oracle in this task uses (1) for determinism.

## Picking EXISTING tags / users vs quick-creating them

Both the `tag_ids` (many2many_tags) and `user_ids` (many2many) autocompletes
include a trailing "Create 'xxx'" (resp. "Create 'xxx' as new user...") entry
when the typed value is not an exact match. An agent that clicks the first
dropdown item without filtering is at risk of creating a brand-new tag/user.

The oracle loops over dropdown items and skips anything containing "Create",
"Start typing", or "Search more" before matching the recognizable substring.
trace_spec forbids `project.tags.create` and `res.users.create` so a
quick-create substitution shows up as a HarmfulWrite.

## Seeding a second internal user for m2m assignee tasks

To make a user pickable in `project.task.user_ids` you need BOTH
`base.group_user` (internal user) AND `project.group_project_user`. The user
must have a login + password even if the seed never logs in as that user —
otherwise the form's name_search filters it out:

```python
env["res.users"].create({
    "name": "Bench Dev 2",
    "login": "bench_dev_2",
    "password": "bench_dev_2",
    "group_ids": [(6, 0, [group_internal.id, group_project_user.id])],
})
```

Use `login` as the canonical identifier in check.py (`user.login ==
'bench_dev_2'`); the display name `Bench Dev 2` may collide with other
benchmark seeds whereas the login is benchmark-owned.

## Cleanup: unlink user -> unlink partner (best effort)

`res.users.unlink()` does NOT cascade-delete the linked `res.partner`; the
partner remains orphaned. In cleanup/seed we attempt `partner.unlink()`
AFTER the user unlink but wrap it in try/except because mail-follower /
activity / message references can block the partner unlink. Leaving an
orphan partner with the canonical `Bench Dev 2` name is harmless for the
benchmark (check.py asserts on `res.users.login`, not on partner existence).
