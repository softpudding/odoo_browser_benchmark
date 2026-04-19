# Cookbook notes for event.create_event_add_question_publish

## `event.event.question_ids` is a Many2many with Add-a-line → SelectCreate

Even though the tab is called "Questions" and UI behaves like a one2many, the
underlying field is Many2many (`event.event.question_ids`) with
`_compute_question_ids` + `readonly=False, store=True`. Clicking **Add a line**
on the list opens the SelectCreate dialog with `domain=[('is_reusable','=',True)]`
and `context={'list_view_ref': 'event.event_question_view_list_add'}`. Inside,
click **New** to fall through to `event_question_view_form` — this is where
the radio `question_type` and the nested Answers notebook live.

Flow chain that BU navigated cleanly single-shot:

1. Tab → Add a line → New
2. Fill Q1 fields → **Save & New** (carries you directly to a fresh
   `event.question` form)
3. Fill Q2 fields (simple_choice) → Answers notebook tab inline-o2m
   **Add a line** for each answer
4. **Save & Close**

## `event.question.question_type = 'text_box'` (NOT 'textbox')

Selection values: `simple_choice`, `text_box`, `name`, `email`, `phone`,
`company_name`. The **label** is "Text Input" but the technical selection key
is `text_box` with the underscore. `check.py` string-equality typos silently
fail — use a constant `Q1_TYPE = "text_box"` and compare.

## `once_per_order` / `is_mandatory_answer` booleans normalize to null

The state-diff engine normalizes False booleans to `null` on the create path.
`expected_state.json` must match with `"norm_value": null` — using `false`
misses the diff and caps F1 at ~0.82 (the other fields still match, but the
two False-boolean edits go in the "extra" bucket).

## Publish path: website_publish_button() sets both flags

`event.event.website_publish_button()` (from `website.published.mixin`)
writes `website_published=True`; the `_inverse_is_published` hook then flips
`is_published=True`. Either UI path works:

- Backend form → click `website_redirect_button` indicator → Owl iframe
  systray toggle (BU handled this with a label-text click on the
  "Unpublished" switch; this is the brittle path for oracle automation).
- Oracle: JSON-RPC `callKw('event.event.website_publish_button')` + a
  defensive `write({is_published: true})` to guarantee both flags in one
  atomic transaction.

## Default question auto-attach does not break the state diff

`_compute_question_ids` attaches 3 `is_default=True` reusable questions
(Name, Email, Phone) to every new event. Our `expected_state.json` only
tracks the TWO new questions we seed; we do NOT assert anything about the
auto-attached ones (state_spec match_key for `event.question` is just
`title`, and we don't list the default titles). check.py uses
`event.question_ids.filtered(lambda q: q.title == ...)` to isolate the
new questions, and a separate guardrail ensures exactly 1 of each.

## Calibration: BU passes single-shot despite hard-tier composite

Despite combining 3 proven-hard patterns (create-from-scratch + nested
o2m within a m2m-create dialog + Owl iframe systray publish), BU solved
this in 19 steps, 141.8s, F1=1.0 on first run. The Odoo 19 event form
is unusually well-labelled for an LLM — every radio has a human-readable
text ("Text Input" / "Selection"), checkboxes surface their text
(`Mandatory`, `Once per Order`), and **Save & New** + **Save & Close**
footer buttons chain the flow cleanly. Harder composites would need:

- Two separate m2m visits for `general_question_ids` (once_per_order=True)
  vs `specific_question_ids` (once_per_order=False) — these fields share
  storage but the form exposes them separately when a task design uses
  an event_type preset.
- A seat-limit + seats_max constraint on the event so
  `_check_seats_availability` fires on save with the right error modal.
- An event.type preset that wipes default questions + requires the agent
  to re-add them.

Task kept as hard/tier:3 with `primary_track: false` given the BU pass.
