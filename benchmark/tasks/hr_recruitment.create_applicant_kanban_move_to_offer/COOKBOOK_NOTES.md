# Cookbook notes — hr_recruitment.create_applicant_kanban_move_to_offer

## Recruitment app entry flow

- `/odoo/recruitment` shows the hr.job kanban. Each `<kanban>` card's
  root action (`type="action"` name=`action_hr_job_applications`, set
  in `addons/hr_recruitment/views/hr_job_views.xml:19`) navigates to
  the Applications kanban of that job. The 3-dot menu on the card has
  a redundant "Applications" link.
- The Applications kanban is defined by `hr_kanban_view_applicant`
  with `default_group_by="stage_id"` and the visible columns are the
  `hr.recruitment.stage` records whose `job_ids` is empty OR contains
  the current job. To force an exact 4-column view per the prompt, the
  seed must attach each canonical stage to the new job via m2m
  `job_ids` (stages with `job_ids=[]` are shared/global and would add
  extra columns).

## Default stages DIFFER from the prompt

- Odoo 19 demo data (`hr_recruitment_data.xml`) installs six global
  stages: `New`, `Qualification`, `First Interview`, `Second
  Interview`, `Contract Proposal`, `Contract Signed`. The prompt asks
  for **`Initial Qualification` / `Qualified` / `Contract Proposal` /
  `Contract Signed`** — so the seed creates its own stages with those
  exact names and pins them to the new job. Two of the names
  (`Contract Proposal`, `Contract Signed`) collide with demo records
  but that is fine: when looking up by `(name, job_ids in job)` the
  newly-created job-scoped records win.

## Kanban quick-create on hr.applicant

- The kanban quick-create view is `quick_create_applicant_form`
  (priority=1000) and exposes only `partner_name` + `job_id`. To fill
  `email_from` and `partner_phone` the user (or oracle) MUST open the
  full form after the quick-create. The oracle clicks the newly-
  created card to open it, then fills those fields and saves. The
  prompt explicitly tells the agent to do the same.
- The Initial Qualification column's `+` button lives inside
  `.o_kanban_header` as `button.o_kanban_quick_add`. Confirm via
  `button.o_kanban_add` (green check) inside `.o_kanban_quick_create`.

## Status bar stage advance

- `hr.applicant.stage_id` is rendered with
  `widget="rotting_statusbar_duration" options="{'clickable': '1'}"`.
  Clicking a stage pill on the form status bar writes `stage_id` and
  (if the new stage has `hired_stage=True`) sets `date_closed`. The
  prompt's target stage `Contract Proposal` has `hired_stage=False`,
  so `date_closed` stays null. The check.py asserts that.

## Phone normalisation

- The form uses `widget="phone"`, which does NOT auto-reformat on
  save — `partner_phone` stores the raw string. The prompt dictates
  `+15555555555` (E.164) and check.py compares after stripping
  whitespace/dashes as a mild allowance for minor UI tweaks. No
  libphonenumber reformat fires in our DB because no country is set
  on the partner at create time.

## Calibration result (medium)

- Oracle: PASS in ~36s, F1=1.0.
- Browser-use: PASS in ~76s, F1=1.0. The task is on the easy side of
  the "medium" band: the quick-create + open-form + status-bar-click
  combo is a linear 3-step flow with no wizard modals and no
  radio-button disambiguation. Tier 2 is appropriate; promoting to
  Tier 3 would require adding a wizard step (e.g. Send email on stage
  transition) or a drag-only constraint.

## state_spec / expected_state

- `hr.applicant` match_key is `partner_name` — unique per run because
  the seed deletes any prior `Alice Applicant`. The created row emits
  6 atomic "create" diffs: `partner_name`, `email_from`,
  `partner_phone`, `stage_id` (Many2one → "Contract Proposal"),
  `job_id` (Many2one → "Bench Senior Dev"), `active` (default True).
  Keep `categ_ids`, `priority`, `user_id`, `kanban_state`, etc. in
  `ignore_fields` to avoid spurious extras.
- No `mail.message` tracking is needed — the task doesn't require a
  message post.
