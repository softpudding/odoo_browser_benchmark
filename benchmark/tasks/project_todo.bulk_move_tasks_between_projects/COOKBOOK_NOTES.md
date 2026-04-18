# project_todo.bulk_move_tasks_between_projects — Odoo 19 quirks

## No bulk "Move to Project" action on project.task in Community

`project.task` in Odoo 19 Community has **no** "Move to Project" /
"Change Project" bulk action in the list / kanban cog Actions menu.
Grepping `addons/project` for `binding_model_id` referencing
`model_project_task` surfaces only a `mail.compose.message` "Send Email"
server action — nothing for reassigning projects in bulk.

The `project_task_view_tree_main_base` list view additionally pins
`project_id` as `readonly="1"` on the column, so **inline multi_edit is
blocked** even though the view declares `multi_edit="1"`. No bulk path
exists at all.

Canonical reassignment workflow: open each task in the form view and
change the `Project` many2one field, then Save. Do the same for every
task you want moved. For tasks that build "move N of M" scenarios, this
forces N separate form-hops — a natural hard-tier workload.

## browser-use misfire: hallucinates access-rights error after first form edit

On the three-tasks-to-move flow, BU succeeded on the first task (Alpha)
and then aborted with:

> I am unable to complete the task because the user 'Mitchell Admin'
> does not have 'write' access to the Task (project.task) model.

This is false — the admin user has full write permission, and the first
write actually went through (state_diff.json confirms Alpha was moved).
BU's own `project_id` autocomplete / save chain tripped on a DOM-detection
issue (`Element and its children (depth 4) are not recognizable dropdown
types` on the `o-autocomplete--input` combobox after a re-render) and it
misattributed the failure to ACL. Partial-completion `{Alpha moved, Bravo
and Charlie in original project}` is the stable BU failure mode here.

Implication for similar tasks: when the workflow requires the same form
edit to be repeated on ≥2 sibling records, expect BU to bail after the
first success with a spurious error, rather than loop. Good hard-tier
fuel. If you want F1 to partial-credit the first completion, leave
`match_key: [name]` on project.task — the engine will still emit
`state_diff_f1 = 0.0` because the scorer binarises on Recall < 1 for
small expected sets (3 edits, 1 matched → 0.33 recall → treated as 0 in
final score field), but Matching=1 shows up in the summary for triage.

## `project.task_count` is computed, not writable

`project.project.task_count` is a `@api.depends('task_ids')` computed
field; it updates automatically when you re-parent tasks via
`project.task.project_id`. check.py should not write to it and should
assert against `search_count` on `project.task` with `project_id=` and
`active=True` filters rather than reading `task_count` directly (the
stored computed value may lag in auto-isolate scenarios).

## seed safety: cascade-delete tasks linked to old projects BEFORE unlinking projects

When rerunning the seed, any prior-run `Bench Proj A` / `Bench Proj B`
record must be unlinked **after** deleting tasks still linked to it,
otherwise `project.project.unlink()` will raise a foreign-key / blocked
related-records error. Pattern used in this seed:

```python
for p in old_projects:
    env["project.task"].with_context(active_test=False).search([
        ("project_id", "=", p.id),
    ]).unlink()
old_projects.unlink()
```

## `state_spec` on project.project: `last_update_status` drifts under active_test

`project.project` exposes a computed `last_update_status` that may switch
value between pre- and post-state captures (status colour computation on
`project.update`). Tracking `project.project` in state_spec.yaml without
adding `last_update_status` to `ignore_fields` produces spurious "edit"
diffs on both Proj A and Proj B even when the agent only touched
`project.task`. Add it to `ignore_fields`.
