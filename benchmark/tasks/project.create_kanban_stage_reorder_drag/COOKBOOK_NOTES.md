# Cookbook notes — project.create_kanban_stage_reorder_drag

## Kanban column quick-create — folded / unfolded state

The right-edge "+/Add column" column in `KanbanRenderer` is rendered by
`web.KanbanColumnQuickCreate`. The folded/unfolded state is encoded as a
**class on the root `.o_column_quick_create` div itself**, NOT on a child:

- folded:  `.o_column_quick_create.o_quick_create_folded`
- unfolded: `.o_column_quick_create.o_quick_create_unfolded`

Consequence: a naive `quick.locator(".o_quick_create_folded")` returns 0
because Playwright treats the locator as a descendant query. Use
`quick.evaluate("(el) => el.classList.contains('o_quick_create_folded')")`
or `.o_column_quick_create.o_quick_create_folded` as a top-level selector.

UI layout:
- Folded: a tall thin column with `<i class="fa fa-angle-double-right"
  aria-label="Add column" title="Add column">` inside `button.o_quick_create_button`.
- Unfolded: `<input type="text" placeholder="Stage...">` +
  `button.o_kanban_add` (green check) + `button.o_kanban_remove` (red x).

## Kanban column drag-reorder — handle and renderer hooks

`KanbanRenderer` calls `useSortable({elements: ".o_group_draggable",
handle: ".o_column_title", ...})` for column reordering. This means:

- The element that must receive the mousedown is `.o_column_title` (the
  header text itself), NOT the whole `.o_kanban_header`.
- The group `.o_kanban_group` must carry class `o_group_draggable`, which
  the renderer adds only when `canResequenceGroups` is true (requires
  `groupsDraggable` on the kanban arch AND a groupable groupBy field).
- On drop, the client calls `list.resequence(movedGroupId, previousGroupId)`
  which POSTs `project.task.type.web_resequence`. `web_resequence` writes
  `sequence` starting at `offset = min(current sequences)` incrementing by 1.

Because of the `offset = min(sequences)` behaviour, if the starting
sequences are sparse (e.g. 10/20/30/40) and the new group has default
`sequence=1`, the FIRST resequence (triggered automatically after
`name_create`) renumbers EVERY group starting at 1, collapsing the
sparse range. A later drag-reorder again resequences the full set.
Consequence: state_spec should **ignore `sequence`** on `project.task.type`
and validate left-to-right order via `check.py` using
`search([...], order='sequence, id')`.

## Browser-use drag-reorder failure mode

BU consistently completes the create-stage step (clicks chevron, types
name, confirms) but fails the subsequent column-drag. Typical outcome:
new stage stays at the far right (position N), even though BU fires
`project.task.type.web_resequence` once (the auto-resequence on create).
The drag gesture either does not fire `dragstart` on the column title,
or drops between wrong columns. This is exactly the "drag-and-drop"
failure pattern flagged in TASK_CREATION_GUIDE.md appendix.

## Seed cleanup for `project.task.type` scoped to a project

`project.task.type` is shared across projects via m2m `project_ids`.
When deleting a project, stages are NOT auto-unlinked — they remain with
an empty `project_ids`. Cleanup pattern:

```python
for stage in stages_scoped:
    stage.write({"project_ids": [(3, project.id)]})
    if not stage.project_ids and stage.name in CANONICAL_NAMES:
        stage.unlink()
```

Restricting the orphan-delete to our canonical names avoids clobbering
stages legitimately shared with other (non-benchmark) projects.

## Expected-state: project.task.type create emits both name and active=true

A freshly-created `project.task.type` shows up in the state diff as TWO
atomic edits even though only `name` is written by `name_create`:

```json
[
  {"field":"name",   "op":"create", "norm_value":"Backlog Review"},
  {"field":"active", "op":"create", "norm_value":true}
]
```

`active` has default=True on the model and the diff engine emits it as a
"create" row alongside `name`. Include both in `expected_state.json` or
the F1 score drops to 0.67 (1 extra unexpected edit).
