# hr_recruitment_survey.attach_survey_require_applicant_submit — Result

- **Task id:** `hr_recruitment_survey.attach_survey_require_applicant_submit`
- **Tier / difficulty:** 2 / medium
- **Oracle:** PASS (25.3s wall clock, 1 atomic edit matches expected)
- **Browser-Use:** PASS (179.7s wall clock, 1/1 atomic edits, F1=1.0)
- **RequiredOpRecall:** 1.0 (no required ops; writes were all non-forbidden)

## What the task actually exercises

1. Recruitment app default view is kanban, and kanban-card click on a
   job opens **Applications** (action `action_hr_job_applications`),
   NOT the job form. The agent must flip to **list view** first or use
   the kanban card's hidden "Configuration" menu. Switching to list
   view via the viewswitcher is the natural path.
2. The `survey_id` many2one on `hr.job` renders inside the Recruitment
   (page name `recruitment_page`, label "Details" in the inherited
   view) notebook tab with a strict domain
   `[('survey_type','=','recruitment')]` — only the seeded
   "Bench Screening" survey (created with `survey_type='recruitment'`)
   shows up. The field carries `context="{'default_access_mode':
   'token'}"` but **no `create="false"`**, so a BU that hallucinates
   "create survey from autocomplete" could in principle pollute state;
   the trace_spec forbids `survey.survey.create` and
   `hr.job.action_new_survey` to guard against that.
3. After `hr.job.survey_id` is written, the related
   `hr.applicant.survey_id` (a `related='job_id.survey_id'` readonly
   m2o) auto-resolves on the applicant form, which in turn unlocks the
   header "Send Interview" button
   (`invisible="not active or not survey_id"`). The task is
   self-verifying: the button's visibility on Alice Candidate is a
   direct visual signal that the survey was attached correctly.

## BU trajectory (single shot)

BU followed the intended path cleanly for the primary objective:
- Step 6: switched to list view via aria-label=List View.
- Step 7: opened "Bench Recruit Lead" row → job form.
- Steps 8–9: typed "Bench Screening" into the `survey_id` input and
  clicked the dropdown option, then clicked Save Manually.
- Steps 10–37: burned ~25 extra steps looking for the Applications
  smart button (BU clicked a decorative container div several times
  before finding the real button), eventually opened the Applications
  kanban, clicked Alice Candidate, and emitted `done`. The Interview
  Form edit was already persisted by step 9.

The state_diff engine sees exactly one atomic edit
(`hr.job.survey_id → 'Bench Screening'` on entity `Bench Recruit
Lead`) and F1 = 1.0.

## Calibration observations

- Medium-tier passing is consistent with row 376
  (`calendar.configure_meeting_with_location_and_reminder`): a
  workflow that is within BU's reach if the notebook tab is correctly
  named and the m2o autocomplete is deterministic.
- To re-tier this upward, one would need to (a) force non-default
  wizard interaction (e.g., the `survey.invite` modal from
  `action_send_survey`), or (b) add a create-from-scratch survey step.
  Both change the task's scope; the current spec stays on the
  canonical "attach existing screening survey" workflow.

## Key cookbook findings

See `COOKBOOK_NOTES.md` for the distilled pointers added to
`benchmark/ODOO19_PATTERNS.md`.
