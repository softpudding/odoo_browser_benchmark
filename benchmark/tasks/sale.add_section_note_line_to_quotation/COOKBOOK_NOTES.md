# Cookbook notes from sale.add_section_note_line_to_quotation

## `<control><create>` renders as sibling `<a>` inside `td.o_field_x2many_list_row_add`

On `sale.order` Order Lines, the XML declares three `<create>` controls
(Add a product, Add a section, Add a note). All three render as
`<a href="#" role="button">` siblings inside the same
`td.o_field_x2many_list_row_add`. The first has no prefix class; the
rest get `ml16`. They are distinguishable **only by text content** —
Playwright's `get_by_role("button", name=..., exact=True)` scoped to
the footer td is the reliable way to hit a specific one.

The default `click_add_a_line` helper in `oracle_helpers.py` prefers
"Add a product" and only falls back to the first `<a>`, which is wrong
for this task. Do NOT use `click_add_a_line` — write a dedicated
`_click_footer_control(page, label)` that locates the footer td and
`get_by_role` filters by exact label.

## After editing a row, leave edit mode *before* clicking a new footer control

If the Order Lines list is in edit mode on one row and you click another
footer `<a>` without first committing/leaving edit mode, the `<a>`'s
click handler can race with the row's blur handler and one of two
things happens:

1. The blur completes, saves the current row, but the `<a>` click is
   eaten — no new row is created.
2. The click lands on a stale `<a>` (the control row re-renders when a
   row is saved, and the node reference Playwright captured is no
   longer in the DOM), so nothing happens visually but the default
   "Add a product" fires.

Reliable recipe before each `_click_footer_control`:
```python
page.locator(".o_form_sheet_bg, .o_form_sheet").first.click(
    position={"x": 5, "y": 5}
)
page.wait_for_timeout(200)
```
This commits the active edit before we go hunt for the footer.

## `sol_text` / `section_and_note_text` field renders different editors per display_type

`SectionAndNoteText.componentToUse`:
- `display_type == 'line_section'` → `CharField` (single-line `<input>`).
- `display_type == 'line_note'` / 'line_subsection' → `TextField`
  (multi-line `<textarea>`).

Oracle/fill code must handle both; `row.locator("input, textarea")` and
picking `.first` works.

## `SectionAndNoteListRenderer.focusToName` auto-focuses the new row's name cell

So right after clicking "Add a section" or "Add a note", the freshly
inserted row is in edit mode and the `name` cell already has focus.
You can type directly via `page.keyboard.type(text)` as a last-ditch
fallback — but first try `row.locator("td[name='name'] input, td[name='name'] textarea")`
for deterministic targeting.

## state diff engine emits ALL tracked fields as separate atomic edits on `op: create`

When `state_spec.fields = [name, display_type, order_id]` and two new
rows are created, the diff engine emits **6** edits (3 fields × 2 rows),
not 2. Your `expected_state.json` must enumerate every tracked field
for every created row; you cannot just expect "the row was created".
Either widen expected_state to all field × row tuples, or narrow
`fields` in state_spec to just the one field that matters (here
`display_type`).

## `order_id` on sale.order.line normalizes to the SO name in state diff

Unlike some other models (`account.move.line.move_id` → null),
`sale.order.line.order_id` normalizes to the parent sale.order's `name`
(e.g. "SO-BENCH-STRUCT"), so you can match on the SO name in
expected_state rather than null.
