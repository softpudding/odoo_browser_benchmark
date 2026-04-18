# hr_skills_survey.link_certification_survey_to_skill — RESULT

## Verdict: REMOVED (feature unavailable — Enterprise-only)

This task is blocked because Odoo 19 **Community** does not expose a
`survey_id` / Certification many2one on `hr.skill`. The skill ↔
certification link that the task prompt describes is an
**Enterprise-only** extension that is not vendored in `addons/` on this
branch.

## Evidence

Inspected `addons/hr_skills_survey/`:

```
addons/hr_skills_survey/
├── __manifest__.py        depends = ['hr_skills', 'survey']
├── models/
│   ├── hr_resume_line.py  # adds survey_id (READONLY) + expiration_status
│   ├── survey_survey.py   # adds certification_validity_months
│   └── survey_user.py     # extends _mark_done() to write hr.resume.line
├── data/hr_resume_data.xml
└── views/
    ├── hr_templates.xml   # inherits resume_line form, shows survey_id
    └── survey_survey_views.xml
```

Key findings:

- `hr.resume.line.survey_id` is declared `readonly=True` — the UI cannot
  write to it; it is set automatically by `survey.user_input._mark_done()`
  when a user submits a passing certification response.
- No module in `addons/` declares `_inherit = 'hr.skill'` adding a
  `survey_id` field (verified via `grep _inherit 'hr.skill'`).
- `hr.skill` itself has only: `name, sequence, skill_type_id, color`.
- The task prompt's "Open skill Python, link the survey in its
  Certification field" step therefore cannot be executed in the
  browser UI — no such field exists on the skill form.

The task's auxiliary workflow (create a certification survey, take it,
observe a cert row populated on the admin's resume) IS feasible in
Community, but (a) the central "link survey to skill" step is not, and
(b) the resume-line population happens via `_mark_done()` as a side
effect, not through an explicit UI action — making the task's key
check (`hr.skill.survey_id` set to the survey) untestable.

## Precedent

Multiple tasks have been Removed on the same grounds (Enterprise-only
addon / feature missing in Community). Most relevant:

- `appointment.public_booking_reschedule_cancel_portal` (row 350) —
  appointment module uninstallable
- `helpdesk.team_sla_assign_escalate_close` (row 351) — helpdesk
  module absent
- `marketing_automation.tag_trigger_drip_campaign` (row 352) —
  marketing_automation absent

All three use the same BLOCKED-skeleton pattern: short-circuit seed /
oracle / check with diagnostic errors, ship empty `expected_state.json`
+ `state_spec: {}` + `trace_spec: []`, STATUS row set to Removed with
`FAIL (module unavailable)`.

## Lifecycle status

- Oracle: did NOT run (short-circuits with RuntimeError).
- BU: did NOT run.
- F1: N/A.
- Calibration: N/A.

## Re-enabling

To re-enable, vendor the enterprise skill-certification link into
`addons/hr_skills_survey/` (or a sibling enterprise module) — specifically
a `_inherit = 'hr.skill'` with a `survey_id = fields.Many2one('survey.survey')`
field and a corresponding view patch on the skill form. Then:

1. Replace the `raise RuntimeError` / `raise NotImplementedError` guards
   in `seed.py` with the real seed (sketch is already in the comment
   block at the bottom of `seed.py`).
2. Flesh out `oracle.py` with the three-phase UI flow documented in
   the module docstring.
3. Flesh out `check.py` to assert the survey exists with
   `survey_type='certification'`, `scoring_success_min>=70.0`, and
   `hr.skill` named Python has `survey_id` pointing to it.
4. Populate `state_spec.yaml` + `expected_state.json` from a real run's
   `state_diff.json`.
5. Flip STATUS row 387 from Removed → WIP and re-run the normal
   lifecycle.
