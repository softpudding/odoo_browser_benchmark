# Cookbook notes — hr_recruitment_survey.attach_survey_require_applicant_submit

New quirks worth preserving in ODOO19_PATTERNS.md (§ Survey + §
hr_recruitment / hr_recruitment_survey):

## hr_recruitment_survey bridge

- `hr_recruitment_survey` is **NOT in the base snapshot**. Seeds must
  `button_immediate_install()` on the module record. `survey` is in
  the base snapshot once early installs complete.
- `hr.job.survey_id` (many2one → `survey.survey`, label
  "Interview Form") is defined by the `hr_recruitment_survey` bridge,
  not by `hr_recruitment` core. The field renders inside the
  Recruitment notebook tab (page name `recruitment_page`, XML label
  "Details" on `hr.view_hr_job_form`) after
  `field[@name='interviewer_ids'] position="after"` — i.e., directly
  under the Hiring Process group.
- The m2o carries `domain="[('survey_type','=','recruitment')]"`
  (defined in `addons/hr_recruitment_survey/views/hr_job_views.xml`).
  A survey created with the default `survey_type='custom'` (or
  `'survey'`, `'assessment'`, `'live_session'`) will **NOT appear** in
  the autocomplete. Seed must create surveys with
  `survey_type='recruitment'` for hr.job to see them.
- `hr.applicant.survey_id` is `related='job_id.survey_id'` (readonly).
  The header "Send Interview" button on the applicant form has
  `invisible="not active or not survey_id"`, so it auto-shows once
  the parent job gets a survey attached — no applicant-level write
  needed.
- The kanban card menu on `hr.job` in recruitment exposes a
  "Interview Form" create-from-scratch action
  (`action_new_survey`) that auto-generates a blank survey titled
  "Interview Form: <job name>" and links it to the job. Tasks that
  want the agent to pick an existing survey must put
  `hr.job.action_new_survey` in `forbidden_ops`, otherwise BU may
  click this menu item and get a cheap "I made a survey" pass.

## Recruitment app navigation trap

- `/odoo/recruitment` opens the **hr.job kanban** (action xmlid
  `hr_recruitment.action_hr_job`). Kanban card click is
  `action="%(action_hr_job_applications)d" type="action"` — it opens
  the **applicants** of that job, not the job form. To reach the job
  form via UI, either (a) switch to list view via the viewswitcher
  and click the row, or (b) open the 3-dots kanban card menu and click
  "Configuration" (`type="open"`, the only kanban path to the form).
  Browser-use empirically finds the viewswitcher path first.

## Recruitment tab rendering

- The "Recruitment" (XML label "Details") and "Summary" notebook
  pages on `hr.view_hr_job_form` default to `invisible="1"` and are
  flipped visible by the `hr_recruitment.hr_job_survey` override —
  but that override gates them with
  `groups="hr_recruitment.group_hr_recruitment_interviewer,hr.group_hr_user"`.
  On a stock `base.user_admin` these are already satisfied in the
  benchmark snapshot, but belt-and-braces seed should still add admin
  to both groups to survive future snapshot drift.

## Survey model re-run cleanup

- `survey.survey.unlink` cascades via a custom cleanup that refuses if
  `user_input_ids` exist — not an issue on fresh seeds. Order in the
  cleanup block:
  1. delete applicants (children)
  2. null out `hr.job.survey_id` then unlink jobs
  3. delete `survey.question` via
     `survey.question_and_page_ids.unlink()` then unlink the survey.
  Reversing 2 and 3 works too but 2-first is cleaner when the survey
  is referenced from the job.
