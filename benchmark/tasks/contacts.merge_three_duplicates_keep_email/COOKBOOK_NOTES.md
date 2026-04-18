# Cookbook notes — contacts.merge_three_duplicates_keep_email

New quirks worth appending to `benchmark/ODOO19_PATTERNS.md`:

## base.partner.merge.automatic.wizard field-precedence semantics

- The wizard `_merge` method delegates value merging to `_update_values`, which
  iterates `itertools.chain(src_partners, [dst_partner])` and for each
  non-x2many/non-computed field writes the *last truthy* value onto the
  destination. That means: when merge sources have DISJOINT non-empty fields
  (e.g. one has email only, another has phone only, dst has neither), the
  final values are deterministic regardless of which partner was picked as
  `dst_partner_id`. There is NO per-field source selection UI in Odoo 19
  (contrary to what some internal docs imply).
- Practical: tasks that want to force the agent to pick a specific
  `dst_partner_id` must assert the surviving record's internal `ref` (or
  another master-specific attribute) in check.py — otherwise any choice of
  master produces the same merged data.

## Merge wizard dst_partner_id dropdown — clearing default value

`div[name='dst_partner_id'] input` arrives pre-filled with the display name
of the last-created partner (via `default_get`). To re-search, you must
actually clear that text first:
- `input.fill("")` alone does not reliably clear (the autocomplete may be
  intercepting keystrokes).
- Safer: `input.click(click_count=3)` to select-all, `page.keyboard.press("Delete")`,
  then `input.fill("")` again, then `input.type(text, delay=40)`.
- Symptom when clearing fails: dropdown shows a single "Create 'X (id)Y'"
  option where `X (id)` is the default and `Y` is your typed text
  concatenated.

## partner_show_db_id display format

`res.partner._compute_display_name` with `partner_show_db_id=True` renders
display_name as `"<name> (<id>)"` (space-paren-id). In `_compute_display_name`
(res_partner.py ~1040), the formatted branch uses tabs and double-dashes,
but the `.o-autocomplete--dropdown-item` renders the non-formatted branch —
so options are `Name (id)`. Parse tail token with `.strip("()")` to recover
the id.

## Merge action (list-view only) binding

`base.action_partner_merge` has `binding_view_types="list,kanban"`, so
Actions > Merge only shows up when you are in list or kanban view of
`res.partner` with multi-select. A form view does NOT surface the Merge
action. Task prompts must explicitly instruct list-view multi-select.
