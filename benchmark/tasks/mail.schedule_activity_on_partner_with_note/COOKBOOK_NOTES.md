# Cookbook notes — mail.schedule_activity_on_partner_with_note

## `mail.activity.schedule` wizard quirks (Odoo 19)

- The chatter **Activity** button opens `mail.activity.schedule` directly
  (no pre-dropdown in v19) when clicked on a record that inherits
  `mail.activity.mixin`. On `res.partner` this works out of the box.
- The wizard's `activity_type_id` defaults to **To-Do**
  (`mail.mail_activity_data_todo`). To-Do's `default_note` is empty and
  `delay_count` is `5` — so the `date_deadline` `_compute_date_deadline`
  pre-fill is **today + 5 days**, NOT today. Prompts that want a specific
  date (e.g. `2026-05-15`) must state it explicitly because the default
  will not match.
- `summary` is a plain `fields.Char`; `note` is `fields.Html`
  (Owl wysiwyg). An agent that does a generic "type into first visible
  field" will land on summary — forcing the note into a different field
  is a latent failure mode for BU. Prompts should label both fields by
  name.
- The footer primary button is `action_schedule_activities` labelled
  **"Schedule"**. It calls
  `_get_applied_on_records().activity_schedule(activity_type_id,
  summary, note, date_deadline, user_id)`, which creates the
  `mail.activity` row directly. No separate save step is required.
- Oracle shortcut: call `res.partner.activity_schedule(...)` via call_kw
  — mirrors the wizard exactly and produces the same end state without
  needing to drive the Owl modal.

## `mail.activity` vs. `mail.activity.type.name='To-Do'`

- The singleton `mail.activity.type` for plain to-dos is stored as
  `"To-Do"` with a hyphen. `env.ref('mail.mail_activity_data_todo')`
  resolves to it. Check.py should compare
  `activity.activity_type_id.name == 'To-Do'` (not `"To Do"`).

## `date_deadline` button-to-input widget

- The wizard renders `date_deadline` as a **read-only button**
  displaying e.g. `"Apr 24"` before any interaction. Clicking it flips
  the node to a visible `<input>` that accepts typed dates in the
  user's locale format (US admin: `MM/DD/YYYY`). Typing a date without
  first clicking the button will miss the input.
- `oracle_helpers.schedule_activity` handles this transition with
  `deadline_widget.locator("button").first.click()` before locating the
  input.

## `note` HTML sanitisation

- Typed plain text becomes `<p>Discuss Q2 plan</p>` after the Owl
  editor wraps it. check.py must strip `<p>`/`<br>` tags (or just
  substring-match `"Q2 plan"`) rather than comparing HTML strings
  verbatim.

## Seed / cleanup idempotence

- `res.partner.unlink` may fail if the partner is referenced elsewhere
  (demo data). Fallback: `write({"active": False})`. Both seed.py and
  cleanup.py guard with try/except.
- Messages (`mail.message`), activities (`mail.activity`), and
  attachments (`ir.attachment`) on the partner must be unlinked BEFORE
  attempting to unlink the partner itself, else Odoo raises FK
  violations on `mail_message.res_id`.
