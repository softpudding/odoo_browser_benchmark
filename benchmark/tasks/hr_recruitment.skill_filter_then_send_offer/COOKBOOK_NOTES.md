# hr_recruitment.skill_filter_then_send_offer — Odoo 19 quirks

## hr_recruitment_skills auto-install

- Both `hr_skills` and `hr_recruitment_skills` declare
  `auto_install: True` in their manifests. Because `hr` is already
  pulled transitively by the base snapshot, both modules come up
  installed in every per-task DB restored from `benchmark_base`.
  Seeds that touch `applicant_skill_ids` / `hr.applicant.skill`
  should still guard with a `button_immediate_install` fallback
  in case a future snapshot is trimmed.

## Send Email action is bound to list/kanban only, NOT form

- `hr_recruitment.action_applicant_send_mail` (server action "Send
  Email") has `binding_view_types="list,kanban"`. It therefore only
  appears in the cog Actions dropdown when the user has selected
  records in the list or kanban view — NOT on the applicant form.
  Tasks that want to exercise this wizard must keep the agent in
  list view and use row-checkbox → Actions menu.
- The wizard model is `applicant.send.mail`, which inherits
  `mail.composer.mixin`. It POSTs `mail.message` records via
  `applicant.message_post(...)` with
  `email_layout_xmlid='mail.mail_notification_light'` and
  `message_type='comment'`. The diff engine sees one `create` per
  tracked field of `mail.message` (subject, model, record_name,
  message_type). `res_id` is run-specific (must go to
  `ignore_fields`).

## Skill search-filter facet

- Installing `hr_recruitment_skills` extends both
  `hr_applicant_view_search` and `hr_applicant_view_search_bis` to
  include `<field name="applicant_skill_ids"/>`. When the user
  types "Python" in the search bar, the autocomplete offers (in
  order): "Search Applicant for: Python", "Search Email for:
  Python", "Search Job Position for: Python", ..., "Search Skills
  for: Python". The Skills row is the one that filters by
  `applicant_skill_ids`. Browser-use tends to pick the first
  autocomplete item (Applicant / Email), so forcing a specific
  facet is a good hard-filter trap when the *other* autocomplete
  options also yield a non-empty (but wrong) list.
- The search view's `<field name="applicant_skill_ids"/>` is a
  one-shot pick — each click adds a facet. There is no multi-skill
  AND operator from the UI; subsequent clicks stack as OR inside
  the same field. Tasks that need multi-skill AND must pre-seed
  an `ir.filters` favorite or phrase the prompt around one skill.

## State-diff entity_key for mail.message

- With `match_key: [record_name, subject]` the diff engine emits
  entity_key `["Alice Senior", "Job Offer - QA Lead"]`. Make sure
  both match-key fields stay listed in `state_spec.yaml.fields` or
  the "create" row fires with nulls.
- Exclude `res_id` from the tracked fields — its numeric value
  depends on which applicant was created first in the per-task DB.
  The deterministic, diff-friendly fields are `subject`, `model`,
  `record_name`, `message_type` (4 atomic edits per offer email).
